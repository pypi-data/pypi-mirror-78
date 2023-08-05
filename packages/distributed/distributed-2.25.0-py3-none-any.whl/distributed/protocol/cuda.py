import dask

from . import pickle
from .serialize import ObjectDictSerializer, register_serialization_family
from dask.utils import typename

cuda_serialize = dask.utils.Dispatch("cuda_serialize")
cuda_deserialize = dask.utils.Dispatch("cuda_deserialize")


def cuda_dumps(x):
    type_name = typename(type(x))
    try:
        dumps = cuda_serialize.dispatch(type(x))
    except TypeError:
        raise NotImplementedError(type_name)

    header, frames = dumps(x)
    header["type-serialized"] = pickle.dumps(type(x))
    header["serializer"] = "cuda"
    header["compression"] = (False,) * len(frames)  # no compression for gpu data
    return header, frames


def cuda_loads(header, frames):
    typ = pickle.loads(header["type-serialized"])
    loads = cuda_deserialize.dispatch(typ)
    return loads(header, frames)


register_serialization_family("cuda", cuda_dumps, cuda_loads)


cuda_object_with_dict_serializer = ObjectDictSerializer("cuda")

cuda_deserialize.register(dict)(cuda_object_with_dict_serializer.deserialize)
