"""Base Dataset classes."""
import warnings
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

import numpy as np
from numpy.random import RandomState, permutation
from tqdm import tqdm

from ..inputs import load, read_abc_string
from ..music import Music
from .utils import download_google_drive_file, download_url, extract_archive

try:
    from torch.utils.data import Dataset as TorchDataset

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import tensorflow as tf
    from tensorflow.data import Dataset as TFDataset

    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False

try:
    from joblib import Parallel, delayed

    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

RemoteDataset_ = TypeVar("RemoteDataset_", bound="RemoteDataset")
FolderDataset_ = TypeVar("FolderDataset_", bound="FolderDataset")


def read_split(filename: Union[str, Path]) -> Dict[str, List[int]]:
    """Read a train-test-validation split from file."""
    indices = {}
    with open(str(filename)) as f:
        for line in f:
            if line.startswith("#"):
                continue
            key, value = line.split(":")
            indices[key] = [int(idx) for idx in value.split(",")]
    return indices


class DatasetInfo:
    """A container for dataset information."""

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        citation: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.homepage = homepage
        self.citation = citation

    def __repr__(self):
        return (
            "DatasetInfo(\n  name={},\n  description={},\n  homepage={},\n  "
            "citation={})".format(
                self.name, self.description, self.homepage, self.citation
            )
        )


class Dataset:
    """Base class for all MusPy datasets.

    To build a custom dataset, it should inherit this class and overide the
    methods ``__getitem__`` and ``__len__`` as well as the class attribute
    ``_info``. ``__getitem__`` should return the ``i``-th data sample as a
    :class:`muspy.Music` object. ``__len__`` should return the size of the
    dataset. ``_info`` should be a :class:`muspy.DatasetInfo` instance
    containing the dataset information.

    """

    _info: DatasetInfo = DatasetInfo()

    def __getitem__(self, index) -> Music:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    @classmethod
    def info(cls):
        """Return the dataset infomation."""
        print(cls._info)

    @classmethod
    def cite(cls):
        """Print the citation infomation."""
        print(cls._info.citation)

    def save(
        self,
        root: Union[str, Path],
        kind: Optional[str] = "json",
        n_jobs: int = 1,
        ignore_exceptions: bool = False,
    ):
        """Save all the music objects to a directory.

        The converted files will be named by its index and saved to ``root/``.

        Parameters
        ----------
        root : str or Path
            Root directory to save the data.
        kind : {'json', 'yaml'}, optional
            File format to save the data. Defaults to 'json'.
        n_jobs : int, optional
            Maximum number of concurrently running jobs in multiprocessing. If
            equal to 1, disable multiprocessing. Defaults to 1.
        ignore_exceptions : bool, optional
            Whether to ignore errors and skip failed conversions. This can be
            helpful if some of the source files is known to be corrupted.
            Defaults to False.

        Notes
        -----
        The original filenames can be found in the ``filenames`` attribute.
        For example, the file at ``filenames[i]`` will be converted and
        saved to ``{i}.json``.

        """
        if kind not in ("json", "yaml"):
            raise TypeError("`kind` must be either 'json' or 'yaml'.")
        if not isinstance(n_jobs, int):
            raise TypeError("`n_jobs` must be an integer.")
        if n_jobs < 0:
            raise ValueError("`n_jobs` must be positive.")

        root = Path(root).expanduser().resolve()
        if not root.exists():
            raise ValueError("`root` must be an existing path.")

        def _saver(idx):
            prefix = "0" * (n_digits - len(str(idx)))
            if ignore_exceptions:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        self[idx].save(
                            root / (prefix + str(idx) + "." + kind), kind
                        )
                except Exception:  # pylint: disable=broad-except
                    return False
                return True
            self[idx].save(root / (prefix + str(idx) + "." + kind), kind)
            return True

        n_digits = len(str(len(self)))

        print("Start converting and saving the dataset.")
        if n_jobs == 1:
            count = 0
            for idx in tqdm(range(len(self))):  # type: ignore
                if _saver(idx):
                    count += 1
        else:
            if not HAS_JOBLIB:
                raise ValueError(
                    "Optional package joblib is required for multiprocessing "
                    "(n_jobs > 1)."
                )
            # TODO: This is slow as `self` is passed between workers.
            results = Parallel(n_jobs=n_jobs, backend="threading", verbose=5)(
                delayed(_saver)(idx) for idx in range(len(self))
            )
            count = results.count(True)
        print(
            "{} out of {} files successfully saved.".format(count, len(self))
        )
        (root / ".muspy.success").touch(exist_ok=True)

    def split(
        self,
        filename: Optional[Union[str, Path]] = None,
        splits: Optional[Union[float, List[float]]] = None,
        random_state: Any = None,
    ) -> Dict[str, List[int]]:
        """Return the dataset as a PyTorch dataset.

        Parameters
        ----------
        filename : str or Path, optional
            If given and exists, path to the file to read the split from.
            If None or not exists, path to save the split.
        splits : float or list of float, optional
            Ratios for train-test-validation splits. If None, return the
            full dataset as a whole. If float, return train and test splits.
            If list of two floats, return train and test splits. If list of
            three floats, return train, test and validation splits.
        random_state : int, array_like or RandomState, optional
            Random state used to create the splits. If int or array_like,
            the value is passed to :class:`numpy.random.RandomState`, and
            the create RandomState object is used to create the splits. If
            RandomState, it will be used to create the splits.

        """
        if filename is not None and Path(filename).is_file():
            return read_split(filename)

        if not isinstance(splits, (float, list, tuple)):
            raise TypeError("`splits` must be of type float, list or tuple.")

        if isinstance(splits, float):
            if splits <= 0:
                raise ValueError("`splits` must be positive.")
            if splits >= 1:
                raise ValueError("`splits` must be less than 1.")
            splits = [splits, 1 - splits]

        if isinstance(splits, (list, tuple)):
            if sum(splits) != 1:
                raise ValueError("`splits` must sum to 1.")
            if len(splits) < 2 or len(splits) > 3:
                raise ValueError("`splits` must have length 2 or 3.")

        if random_state is None:
            rand_indices = permutation(len(self))
        else:
            if not isinstance(random_state, RandomState):
                random_state = RandomState(random_state)
            rand_indices = random_state.permutation(len(self))

        boundaries = np.cumsum([0.0] + list(splits))
        names = ("train", "test", "validation")
        indices = {}
        for idx, (start, end) in enumerate(
            zip(boundaries[:-1], boundaries[1:])
        ):
            start_idx = int(start * len(self))
            end_idx = int(end * len(self))
            indices[names[idx]] = rand_indices[start_idx:end_idx]

        if filename is not None:
            with open(str(filename), "w") as f:
                f.write("# {}\n".format(splits))
                for key, value in indices.items():
                    f.write(
                        "{}: {}\n".format(
                            key, ", ".join(str(idx) for idx in value)
                        )
                    )

        return indices

    def to_pytorch_dataset(
        self,
        factory: Optional[Callable] = None,
        representation: Optional[str] = None,
        split_filename: Optional[Union[str, Path]] = None,
        splits: Optional[Union[float, List[float]]] = None,
        random_state: Any = None,
        **kwargs: Any
    ) -> Union["TorchDataset", Dict[str, "TorchDataset"]]:
        """Return the dataset as a PyTorch dataset.

        Parameters
        ----------
        factory : Callable, optional
            Function to be applied to the Music objects. The input is a Music
            object, and the output is an array or a tensor.
        representation : str, optional
            Target representation. Supported values are 'event', 'note',
            'pianoroll', 'monotoken' and 'polytoken'.
        split_filename : str or Path, optional
            If given and exists, path to the file to read the split from.
            If None or not exists, path to save the split.
        splits : float or list of float, optional
            Ratios for train-test-validation splits. If None, return the
            full dataset as a whole. If float, return train and test splits.
            If list of two floats, return train and test splits. If list of
            three floats, return train, test and validation splits.
        random_state : int, array_like or RandomState, optional
            Random state used to create the splits. If int or array_like,
            the value is passed to :class:`numpy.random.RandomState`, and
            the create RandomState object is used to create the splits. If
            RandomState, it will be used to create the splits.

        Returns
        -------
        :class:torch.utils.data.Dataset` or Dict of
        :class:torch.utils.data.Dataset`
            Converted PyTorch dataset(s).

        """
        if representation is None and factory is None:
            raise TypeError(
                "One of `representation` and `factory` must be given."
            )
        if representation is not None and factory is not None:
            raise TypeError(
                "Only one of `representation` and `factory` can be given."
            )

        if not HAS_TORCH:
            raise ImportError("Optional package torch is required.")

        # No split
        if splits is None:
            if representation is not None:
                return TorchRepresentationDataset(
                    self, representation, **kwargs
                )
            return TorchMusicFactoryDataset(self, factory)  # type: ignore

        datasets: Dict[str, TorchDataset] = {}
        indices_list = self.split(split_filename, splits, random_state)
        for key, value in indices_list.items():
            if representation is not None:
                datasets[key] = TorchRepresentationDataset(
                    self, representation, key, value, **kwargs,
                )
            else:
                datasets[key] = TorchMusicFactoryDataset(
                    self, factory, key, value,  # type: ignore
                )

        return datasets

    def to_tensorflow_dataset(
        self,
        factory: Optional[Callable] = None,
        representation: Optional[str] = None,
        split_filename: Optional[Union[str, Path]] = None,
        splits: Optional[Union[float, List[float]]] = None,
        random_state: Any = None,
        **kwargs: Any
    ) -> Union["TFDataset", Dict[str, "TFDataset"]]:
        """Return the dataset as a TensorFlow dataset.

        Parameters
        ----------
        factory : Callable, optional
            Function to be applied to the Music objects. The input is a Music
            object, and the output is an array or a tensor.
        representation : str, optional
            Target representation. Supported values are 'event', 'note',
            'pianoroll', 'monotoken' and 'polytoken'.
        split_filename : str or Path, optional
            If given and exists, path to the file to read the split from.
            If None or not exists, path to save the split.
        splits : float or list of float, optional
            Ratios for train-test-validation splits. If None, return the
            full dataset as a whole. If float, return train and test splits.
            If list of two floats, return train and test splits. If list of
            three floats, return train, test and validation splits.
        random_state : int, array_like or RandomState, optional
            Random state used to create the splits. If int or array_like,
            the value is passed to :class:`numpy.random.RandomState`, and
            the create RandomState object is used to create the splits. If
            RandomState, it will be used to create the splits.

        Returns
        -------
        :class:tensorflow.data.Dataset` or Dict of
        :class:tensorflow.data.dataset`
            Converted TensorFlow dataset(s).

        """
        if representation is None and factory is None:
            raise TypeError(
                "One of `representation` and `factory` must be given."
            )
        if representation is not None and factory is not None:
            raise TypeError(
                "Only one of `representation` and `factory` can be given."
            )

        if not HAS_TENSORFLOW:
            raise ImportError("Optional package tensorflow is required.")

        if representation is not None:

            def _gen(indices):
                for idx in indices:
                    yield self[idx].to_representation(representation, **kwargs)

        else:

            def _gen(indices):
                for idx in indices:
                    yield factory(self[idx])

        # TODO: `from_generator` is slow.

        # No split
        if splits is None:
            indices = np.arange(len(self))
            return TFDataset.from_generator(_gen, tf.float32, args=[indices])

        datasets: Dict[str, TFDataset] = {}
        indices_list = self.split(split_filename, splits, random_state)
        for key, value in indices_list.items():
            indices = np.array(value)
            datasets[key] = TFDataset.from_generator(
                _gen, tf.float32, args=[indices]
            )

        return datasets


class RemoteDataset(Dataset):
    """Base class for remote MusPy datasets.

    This class is extended from :class:`muspy.Dataset` to support remote
    datasets. To build a custom dataset based on this class, please refer to
    :class:`muspy.Dataset` for the docmentation of the methods
    ``__getitem__`` and ``__len__``, and the class attribute ``_info``. In
    addition, the class attribute ``_sources`` containing the URLs to the
    source files should be properly set (see Notes).

    Attributes
    ----------
    root : str or Path
        Root directory of the dataset.

    Parameters
    ----------
    download_and_extract : bool, optional
        Whether to download and extract the dataset. Defaults to False.
    cleanup : bool, optional
        Whether to remove the original archive(s). Defaults to False.

    Raises
    ------
    RuntimeError:
        If ``download_and_extract`` is False but file
        ``{root}/.muspy.success`` does not exist (see below).

    Important
    ---------
    :meth:`muspy.Dataset.exists` depends solely on a special file named
    ``.muspy.success`` in the folder ``{root}/``, which serves as an
    indicator for the existence and integrity of the dataset. This file will
    automatically be created if the dataset is successfully downloaded and
    extracted by :meth:`muspy.Dataset.download_and_extract`.

    If the dataset is downloaded manually, make sure to create the
    ``.muspy.success`` file in the folder ``{root}/`` to prevent errors.

    Notes
    -----
    The class attribute ``_sources`` is a dictionary containing the
    following information of each source file.

    - filename (str): Name to save the file.
    - url (str): URL to the file.
    - archive (bool): Whether the file is an archive.
    - md5 (str, optional): Expected MD5 checksum of the file.

    Here is an example.::

        _sources = {
            "example": {
                "filename": "example.tar.gz",
                "url": "https://www.example.com/example.tar.gz",
                "archive": True,
                "md5": None,
            }
        }

    See Also
    --------
    :class:`muspy.Dataset` : The base class for all MusPy datasets.

    """

    _sources: Dict[str, dict] = {}

    def __init__(
        self,
        root: Union[str, Path],
        download_and_extract: bool = False,
        cleanup: bool = False,
    ):
        super().__init__()
        self.root = Path(root).expanduser().resolve()
        if not self.root.exists():
            raise ValueError("`root` must be an existing path.")
        if not self.root.is_dir():
            raise ValueError("`root` must be a directory.")

        if download_and_extract:
            self.download_and_extract(cleanup)

        if not self.exists():
            raise RuntimeError(
                "Dataset not found. You can download it by passing "
                "`download_and_extract=True`."
            )

    def __repr__(self) -> str:
        return "{}(root={})".format(type(self).__name__, self.root)

    def __getitem__(self, index) -> Music:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def exists(self) -> bool:
        """Return True if the dataset exists, otherwise False."""
        if not (self.root / ".muspy.success").is_file():
            return False
        return True

    def source_exists(self) -> bool:
        """Return True if all the sources exist, otherwise False."""
        for source in self._sources.values():
            filename = self.root / source["filename"]
            if not filename.is_file():
                return False
            if "size" in source and filename.stat().st_size != source["size"]:
                return False
        return True

    def download(self: RemoteDataset_) -> RemoteDataset_:
        """Download the source datasets."""
        for source in self._sources.values():
            filename = self.root / source["filename"]
            md5 = source.get("md5")

            if filename.is_file():
                if (
                    "size" not in source
                    or filename.stat().st_size == source["size"]
                ):
                    print(
                        "Skip existing source : {}.".format(
                            source["filename"]
                        )
                    )
                    continue
                print("Source file is found but corrupted.")

            print("Start downloading source : {}.".format(source["filename"]))
            if source.get("google_drive_id") is not None:
                download_google_drive_file(
                    source["google_drive_id"], filename, md5
                )
            else:
                download_url(source["url"], filename, md5)
        return self

    def extract(self: RemoteDataset_, cleanup: bool = False) -> RemoteDataset_:
        """Extract the downloaded archive(s).

        Parameters
        ----------
        cleanup : bool, optional
            Whether to remove the original archive. Defaults to False.

        """
        for source in self._sources.values():
            filename = self.root / source["filename"]
            if source["archive"]:
                print("Start extracting archive : {}.".format(source["filename"]))
                extract_archive(filename, self.root, cleanup=cleanup)
        (self.root / ".muspy.success").touch(exist_ok=True)
        return self

    def download_and_extract(
        self: RemoteDataset_, cleanup: bool = False
    ) -> RemoteDataset_:
        """Extract the downloaded archives.

        This is equivalent to ``RemoteDataset.download().extract(cleanup)``.

        Parameters
        ----------
        cleanup : bool, optional
            Whether to remove the original archive. Defaults to False.

        """
        return self.download().extract(cleanup)


if HAS_TORCH:

    class TorchMusicFactoryDataset(TorchDataset):
        """A PyTorch dataset built from a Music dataset.

        Parameters
        ----------
        dataset : :class:`muspy.Dataset`
            Dataset object to base on.
        factory : Callable
            Function to be applied to the Music objects. The input is a Music
            object, and the output is an array or a tensor.

        """

        def __init__(
            self,
            dataset: Dataset,
            factory: Callable,
            subset: str = "Full",
            indices: Optional[List[int]] = None,
        ):
            self.dataset = dataset
            self.factory = factory
            self.subset = subset
            self.indices = indices
            if self.indices is not None:
                self.indices = sorted(
                    idx for idx in self.indices if idx < len(self.dataset)
                )

        def __repr__(self):
            return (
                "TorchMusicFactoryDataset(dataset={}, factory={}, subset={})"
                "".format(self.dataset, self.subset, self.factory)
            )

        def __getitem__(self, index):
            if self.indices is None:
                return self.factory(self.dataset[index])
            return self.factory(self.dataset[self.indices[index]])

        def __len__(self) -> int:
            if self.indices is None:
                return len(self.dataset)
            return len(self.indices)

    class TorchRepresentationDataset(TorchMusicFactoryDataset):
        """A PyTorch music dataset.

        Parameters
        ----------
        dataset : :class:`muspy.Dataset`
            Dataset object to base on.
        representation : str
            Target representation. Supported values are 'event', 'note',
            'pianoroll', 'monotoken' and 'polytoken'.

        """

        def __init__(
            self,
            dataset: Dataset,
            representation: str,
            subset: str = "Full",
            indices: Optional[List[int]] = None,
            **kwargs: Any
        ):
            self.representation = representation

            def factory(music):
                return music.to_representation(representation, **kwargs)

            super().__init__(dataset, factory, subset, indices)

        def __repr__(self):
            return (
                "TorchRepresentationDataset(dataset={}, representation={}, "
                "subset={})".format(
                    self.dataset, self.representation, self.subset
                )
            )


class MusicDataset(Dataset):
    """A local dataset containing MusPy JSON/YAML files in a folder.

    Attributes
    ----------
    root : str or Path
        Root directory of the dataset.
    kind : {'json', 'yaml'}, optional
        File format of the data. Defaults to 'json'.

    """

    def __init__(self, root: Union[str, Path], kind: str = "json"):
        self.root = Path(root).expanduser().resolve()
        if not self.root.exists():
            raise ValueError("`root` must be an existing path.")
        if not self.root.is_dir():
            raise ValueError("`root` must be a directory.")

        self.kind = kind
        self.filenames = sorted(self.root.rglob("*." + self.kind))

    def __repr__(self) -> str:
        return "{}(root={})".format(type(self).__name__, self.root)

    def __getitem__(self, index) -> Music:
        return load(self.root / self.filenames[index], self.kind)

    def __len__(self) -> int:
        return len(self.filenames)


class RemoteMusicDataset(MusicDataset, RemoteDataset):
    """A dataset containing MusPy JSON/YAML files in a folder.

    This class extended :class:`muspy.RemoteDataset` and
    :class:`muspy.FolderDataset`. Please refer to their documentation for
    details.

    Attributes
    ----------
    root : str or Path
        Root directory of the dataset.
    kind : {'json', 'yaml'}, optional
        File format of the data. Defaults to 'json'.

    Parameters
    ----------
    download_and_extract : bool, optional
        Whether to download and extract the dataset. Defaults to False.
    cleanup : bool, optional
        Whether to remove the original archive(s). Defaults to False.

    """

    def __init__(
        self,
        root: Union[str, Path],
        download_and_extract: bool = False,
        cleanup: bool = False,
        kind: str = "json",
    ):
        RemoteDataset.__init__(self, root, download_and_extract, cleanup)
        MusicDataset.__init__(self, root, kind)


class FolderDataset(Dataset):
    """A class of datasets containing files in a folder.

    Two modes are available for this dataset. When the on-the-fly mode is
    enabled, a data sample is converted to a music object on the fly when
    being indexed. When the on-the-fly mode is disabled, a data sample is
    loaded from the precomputed converted data.

    Attributes
    ----------
    root : str or Path
        Root directory of the dataset.

    Parameters
    ----------
    convert : bool, optional
        Whether to convert the dataset to MusPy JSON/YAML files. If False,
        will check if converted data exists. If so, disable on-the-fly mode.
        If not, enable on-the-fly mode and warns. Defaults to False.
    kind : {'json', 'yaml'}, optional
        File format to save the data. Defaults to 'json'.
    n_jobs : int, optional
        Maximum number of concurrently running jobs in multiprocessing. If
        equal to 1, disable multiprocessing. Defaults to 1.
    ignore_exceptions : bool, optional
        Whether to ignore errors and skip failed conversions. This can be
        helpful if some of the source files is known to be corrupted.
        Defaults to False.
    use_converted : bool, optional
        Force to disable on-the-fly mode and use stored converted data

    Important
    ---------
    :meth:`muspy.FolderDataset.converted_exists` depends solely on a
    special file named ``.muspy.success`` in the folder
    ``{root}/_converted/``, which serves as an indicator for the existence
    and integrity of the converted dataset. If the converted dataset is
    built by :meth:`muspy.FolderDataset.convert`, the ``.muspy.success``
    file will be created as well. If the converted dataset is created
    manually, make sure to create the ``.muspy.success`` file in the folder
    ``{root}/_converted/`` to prevent errors.

    Notes
    -----
    This class is extended from :class:`muspy.Dataset`. To build a custom
    dataset based on this class, please refer to :class:`muspy.Dataset` for
    the docmentation of the methods ``__getitem__`` and ``__len__``, and the
    class attribute ``_info``.

    In addition, the attribute ``_extension`` and method ``read`` should be
    properly set. ``_extension`` is the extension to look for when building
    the dataset. All files with the given extension will be included as
    source files. ``read`` is a callable that takes as inputs a filename of
    a source file and return the converted Music object.

    See Also
    --------
    :class:`muspy.Dataset` : The base class for all MusPy datasets.

    """

    _extension: str = ""

    def __init__(
        self,
        root: Union[str, Path],
        convert: bool = False,
        kind: str = "json",
        n_jobs: int = 1,
        ignore_exceptions: bool = False,
        use_converted: Optional[bool] = None,
    ):
        self.root = Path(root).expanduser().resolve()
        self.kind = kind

        # An internal pointer to the callable used to produce the Music object
        self._factory: Callable = lambda: None

        # An internal pointer to the list of filenames used when indexing
        self._filenames: list = []

        self.raw_filenames: list = []
        self.converted_filenames: list = []

        if convert:
            self.convert(kind, n_jobs, ignore_exceptions)

        if use_converted is None:
            use_converted = self.converted_exists()

        if use_converted:
            self.use_converted()
        else:
            self.on_the_fly()

        if not self._filenames:
            raise ValueError("Nothing found in the directory.")

        (self.root / ".muspy.success").touch()

    def __repr__(self) -> str:
        return "{}(root={})".format(type(self).__name__, self.root)

    def __getitem__(self, index) -> Music:
        return self._factory(self._filenames[index])

    def __len__(self) -> int:
        return len(self._filenames)

    def read(self, filename: Any) -> Music:
        """Read a file into a Music object."""
        raise NotImplementedError

    def load(self, filename: Union[str, Path]) -> Music:
        """Read a file into a Music object."""
        return load(self.root / filename)

    def exists(self) -> bool:
        """Return True if the dataset exists, otherwise False."""
        if not (self.root / ".muspy.success").is_file():
            return False
        return True

    @property
    def converted_dir(self):
        """Return the path to the root directory of the converted dataset."""
        return self.root / "_converted"

    def converted_exists(self) -> bool:
        """Return True if the saved dataset exists, otherwise False."""
        if not (self.converted_dir / ".muspy.success").is_file():
            return False
        return True

    def use_converted(self: FolderDataset_) -> FolderDataset_:
        """Disable on-the-fly mode and use converted data."""
        if not self.converted_exists():
            raise RuntimeError(
                "Converted data not found. Run `convert()` to convert "
                "the dataset."
            )
        if not self.converted_filenames:
            self.converted_filenames = sorted(
                self.converted_dir.rglob("*." + self.kind)
            )
        self._filenames = self.converted_filenames
        self._use_converted = True
        self._factory = self.load
        return self

    def on_the_fly(self: FolderDataset_) -> FolderDataset_:
        """Enable on-the-fly mode and convert the data on the fly."""
        if not self.raw_filenames:
            self.raw_filenames = sorted(
                (
                    filename
                    for filename in self.root.rglob("*." + self._extension)
                    if not str(filename.relative_to(self.root)).startswith(
                        "_converted/"
                    )
                )
            )
        self._filenames = self.raw_filenames
        self._use_converted = False
        self._factory = self.read
        return self

    def convert(
        self: FolderDataset_,
        kind: str = "json",
        n_jobs: int = 1,
        ignore_exceptions: bool = False,
    ) -> FolderDataset_:
        """Convert and save the Music objects.

        The converted files will be named by its index and saved to
        ``root/_converted``. The original filenames can be found in the
        ``filenames`` attribute. For example, the file at ``filenames[i]``
        will be converted and saved to ``{i}.json``.

        Parameters
        ----------
        kind : {'json', 'yaml'}, optional
            File format to save the data. Defaults to 'json'.
        n_jobs : int, optional
            Maximum number of concurrently running jobs in multiprocessing. If
            equal to 1, disable multiprocessing. Defaults to 1.
        ignore_exceptions : bool, optional
            Whether to ignore errors and skip failed conversions. This can be
            helpful if some of the source files is known to be corrupted.
            Defaults to False.

        """
        if self.converted_exists():
            print("Skip conversion as the target folder exists.")
            return self
        self.on_the_fly()
        self.converted_dir.mkdir(exist_ok=True)
        self.save(self.converted_dir, kind, n_jobs, ignore_exceptions)
        self.use_converted()
        self.kind = kind
        return self


class RemoteFolderDataset(FolderDataset, RemoteDataset):
    """A class of remote datasets containing files in a folder.

    This class extended :class:`muspy.RemoteDataset` and
    :class:`muspy.FolderDataset`. Please refer to their documentation for
    details.

    Attributes
    ----------
    root : str or Path
        Root directory of the dataset.

    Parameters
    ----------
    download_and_extract : bool, optional
        Whether to download and extract the dataset. Defaults to False.
    cleanup : bool, optional
        Whether to remove the original archive(s). Defaults to False.
    convert : bool, optional
        Whether to convert the dataset to MusPy JSON/YAML files. If False,
        will check if converted data exists. If so, disable on-the-fly mode.
        If not, enable on-the-fly mode and warns. Defaults to False.
    kind : {'json', 'yaml'}, optional
        File format to save the data. Defaults to 'json'.
    n_jobs : int, optional
        Maximum number of concurrently running jobs in multiprocessing. If
        equal to 1, disable multiprocessing. Defaults to 1.
    ignore_exceptions : bool, optional
        Whether to ignore errors and skip failed conversions. This can be
        helpful if some of the source files is known to be corrupted.
        Defaults to False.
    use_converted : bool, optional
        Force to disable on-the-fly mode and use stored converted data

    See Also
    --------
    :class:`muspy.RemoteDataset` : Base class for remote MusPy datasets.
    :class:`muspy.FolderDataset` : A class of datasets containing files in a
      folder.

    """

    def __init__(
        self,
        root: Union[str, Path],
        download_and_extract: bool = False,
        cleanup: bool = False,
        convert: bool = False,
        kind: str = "json",
        n_jobs: int = 1,
        ignore_exceptions: bool = False,
        use_converted: Optional[bool] = None,
    ):
        RemoteDataset.__init__(self, root, download_and_extract, cleanup)
        FolderDataset.__init__(
            self, root, convert, kind, n_jobs, ignore_exceptions, use_converted
        )

    def read(self, filename: str) -> Music:
        """Read a file into a Music object."""
        raise NotImplementedError


class ABCFolderDataset(FolderDataset):
    """A class of local datasets containing ABC files in a folder."""

    _extension = "abc"

    def read(self, filename: Tuple[str, Tuple[int, int]]) -> Music:
        """Read a file into a Music object."""
        filename_, (start, end) = filename
        data = []
        with open(filename_) as f:
            for idx, line in enumerate(f):
                if start <= idx < end and not line.startswith("%"):
                    data.append(line)
        return read_abc_string("".join(data))[0]

    def on_the_fly(self: FolderDataset_) -> FolderDataset_:
        """Enable on-the-fly mode and convert the data on the fly."""
        if not self.raw_filenames:
            filenames = sorted(
                (
                    filename
                    for filename in self.root.rglob("*." + self._extension)
                    if not str(filename.relative_to(self.root)).startswith(
                        "_converted/"
                    )
                )
            )
            self.raw_filenames = []
            for filename in filenames:
                idx = 0
                start = 0
                with open(filename, errors="ignore") as f:

                    # Detect parts in a file
                    for idx, line in enumerate(f):
                        if line.startswith("X:"):
                            if start:
                                self.raw_filenames.append(
                                    (filename, (start, idx))
                                )
                            start = idx

                    # Append the last part
                    if start:
                        self.raw_filenames.append((filename, (start, idx)))

        self._filenames = self.raw_filenames
        self._use_converted = False
        self._factory = self.read
        return self


class RemoteABCFolderDataset(ABCFolderDataset, RemoteDataset):
    """A class of remote datasets containing ABC files in a folder."""

    def __init__(
        self,
        root: Union[str, Path],
        download_and_extract: bool = False,
        cleanup: bool = False,
        convert: bool = False,
        kind: str = "json",
        n_jobs: int = 1,
        ignore_exceptions: bool = False,
        use_converted: Optional[bool] = None,
    ):
        RemoteDataset.__init__(self, root, download_and_extract, cleanup)
        ABCFolderDataset.__init__(
            self, root, convert, kind, n_jobs, ignore_exceptions, use_converted
        )
