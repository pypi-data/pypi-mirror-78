from pulr import config, register_puller, set_data

from pulr.dp import (parse_int, prepare_transform, run_transform, DATA_TYPE_BIT,
                     DATA_TYPE_INT16, DATA_TYPE_INT32, DATA_TYPE_REAL32,
                     DATA_TYPE_UINT16, DATA_TYPE_UINT32, DATA_TYPE_UINT64,
                     DATA_TYPE_INT8, DATA_TYPE_UINT8)

from functools import partial
import ctypes
import platform

import jsonschema

plc_timeout = 2000
plc_path = ''
plc_lib = None

active_tags = {}

SCHEMA_PROTO = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'enum': ['enip/ab_eip']
        },
        'source': {
            'type': 'string'
        },
        'path': {
            'type': 'string'
        },
        'cpu': {
            'type': 'string',
            'enum': ['LGX', 'MLGX', 'PLC', 'MLGX800']
        }
    },
    'additionalProperties': False,
    'required': ['name', 'source', 'cpu']
}

SCHEMA_PULL = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'tag': {
                'type': 'string'
            },
            'size': {
                'type': 'integer',
                'minimal': 1
            },
            'count': {
                'type': 'integer',
                'minimal': 1
            },
            'process': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'offset': {
                            'type': ['integer', 'string'],
                        },
                        'set-id': {
                            'type': 'string',
                        },
                        'type': {
                            'type':
                                'string',
                            'enum': [
                                'real', 'real32', 'uint16', 'word', 'uint32',
                                'dword', 'sint16', 'int16', 'sint32', 'int32',
                                'uint8', 'int8', 'sint8', 'byte'
                            ]
                        },
                        'transform': {
                            'type': 'array'
                        }
                    },
                    'additionalProperties': False,
                    'required': ['offset', 'type', 'set-id']
                }
            }
        },
        'additionalProperties': False,
        'required': ['tag', 'process']
    }
}


def parse_offset(offset):
    if isinstance(offset, int):
        ofs = offset
    else:
        ofs = 0
        for x in offset.split('+'):
            ofs += int(x.strip())
    return ofs


def init(cfg_proto, cfg_pull, timeout=5):
    global plc_timeout, plc_path, plc_lib

    system = platform.system()
    if system == 'Windows':
        libfile = 'plctag.dll'
    elif system == 'Darwin':
        libfile = 'libplctag.dylib'
    else:
        libfile = 'libplctag.so'
    plc_lib = ctypes.cdll.LoadLibrary(library)

    jsonschema.validate(cfg_proto, SCHEMA_PROTO)
    jsonschema.validate(cfg_pull, SCHEMA_PULL)
    if cfg_proto['name'] in ['enip/ab_eip']:
        try:
            host, port = cfg_proto['source'].rsplit(':', 1)
        except:
            host = cfg_proto['source']
            port = 44818
    else:
        raise ValueError(f'Unsupported protocol: {cfg_proto["name"]}')

    path = cfg_proto.get('path', '')

    cpu = cfg_proto['cpu']

    plc_timeout = ctypes.c_int(timeout * 1000)

    plc_path = f'protocol={ab_eip}&gateway={host}:{port}&path={path}&cpu={cpu}'

    for p in cfg_pull:
        tag = p['tag']
        size = p.get('size', 1)
        count = p.get('count')
        tag_path = f'&elem_size={size}'
        if count:
            tag_path += f'&elem_count={count}'
        tag_path += f'&name={tag}'
        pmap = []
        for m in p.get('process', []):
            offset = m['offset']
            o = m['set-id']
            tp = m.get('type')
            transform = m.get('transform')
            if reg[0] in ['h', 'i']:
                offset = parse_offset(offset)
                if tp in ['real', 'real32']:
                    fn = partial(real32_to_data, o, offset,
                                 prepare_transform(o, transform))
                elif tp in ['sint8', 'int8']:
                    fn = partial(int8_to_data, o, offset,
                                 prepare_transform(o, transform))
                elif tp in ['uint8', 'byte']:
                    fn = partial(uint8_to_data, o, offset,
                                 prepare_transform(o, transform))
                elif not tp or tp in ['uint16', 'word']:
                    fn = partial(uint16_to_data, o, offset,
                                 prepare_transform(o, transform))
                elif tp in ['uint32', 'dword']:
                    fn = partial(uint32_to_data, o, offset,
                                 prepare_transform(o, transform))
                elif tp in ['sint16', 'int16']:
                    fn = partial(int16_to_data, o, offset,
                                 prepare_transform(o, transform))
                elif tp in ['sint32', 'int32']:
                    fn = partial(int32_to_data, o, offset,
                                 prepare_transform(o, transform))
                else:
                    raise ValueError(f'type unsupported: {tp}')
            pmap.append(fn)
        register_puller(partial(read_tag, tag_path), pmap)
    register_cleaner(clear_tags)


def shutdown():
    for p, t in active_tags.items():
        plc_lib.plc_tag_destroy(t)
    active_tags.clear()
