from os import path

import yt_dlp
import yt_dlp.options

import config

create_parser = yt_dlp.options.create_parser

final_filename = None

def ydl_post_hook(d):
    global final_filename
    final_filename = d

std_opts = {
    'ignoreerrors': False,
    'retries': 0,
    'fragment_retries': 0,
    'exctract_flat': False,
    'concat_playlist': 'never',
    'update_self': False,
    'post_hooks': [ydl_post_hook],
    'paths': {'home': './storage/ydl'},
}

f_opts = {
    'path': {'home': path.join(config.STORAGE_PATH, 'ydl')},
}

def update_opts(opts):
    for k, v in std_opts.items():
        if k not in opts.keys():
            opts[k] = v

    # Forcefully update required options
    for k, v in f_opts.items():
        opts[k] = v

    return opts

def parse_patched_options(opts):
    patched_parser = create_parser()
    patched_parser.defaults.update({})
    yt_dlp.options.create_parser = lambda: patched_parser
    try:
        return yt_dlp.parse_options(opts)
    finally:
        yt_dlp.options.create_parser = create_parser

default_opts = parse_patched_options([]).ydl_opts

def cli_to_api(opts):
    opts = yt_dlp.parse_options(opts).ydl_opts

    diff = {k: v for k, v in opts.items() if default_opts[k] != v}
    if 'postprocessors' in diff:
        diff['postprocessors'] = [pp for pp in diff['postprocessors']
                                  if pp not in default_opts['postprocessors']]

    return diff

def ydl_get_title(link):
    info = None
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(link, download=False)
    return info['title']


def ydl_download(opts, link) -> str:
    global final_filename

    #opts = update_opts(opts)

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            error_code = ydl.download(link)
        except AttributeError:
            return None

    return final_filename
