#!/usr/bin/env python
"""
Generate pseudo-NSBundles for use in iOS SDKs.

Useful for bundling images, strings files, and other assets into a compiled iOS static library.
The generated code has special support for bundled images, analogous to UIImage's +imageNamed:.
"""

from __future__ import division

import hashlib
import os
import sys
import time
import zlib

import argparse
import biplist
import jinja2


def paths_in_directory(input_directory):
    """
    Generate a list of all files in input_directory, each as a list containing path components.
    """
    paths = []
    for base_path, directories, filenames in os.walk(input_directory):
        relative_path = os.path.relpath(base_path, input_directory)
        path_components = relative_path.split(os.sep)
        if path_components[0] == ".":
            path_components = path_components[1:]
        if path_components and path_components[0].startswith("."):
            # hidden dir
            continue
        path_components = filter(bool, path_components)  # remove empty components
        for filename in filenames:
            if filename.startswith("."):
                # hidden file
                continue
            paths.append(path_components + [filename])
    return paths


def static_uint8_variable_for_data(variable_name, data, max_line_length=120, comment="", indent=2):
    r"""
    >>> static_uint8_variable_for_data("v", "abc")
    'static uint8_t v[3] = {\n  0x61, 0x62, 0x63,\n}; // v'
    >>> static_uint8_variable_for_data("v", "abc", comment="hi")
    'static uint8_t v[3] = { // hi\n  0x61, 0x62, 0x63,\n}; // v'
    >>> static_uint8_variable_for_data("v", "abc", indent=4)
    'static uint8_t v[3] = {\n    0x61, 0x62, 0x63,\n}; // v'
    >>> static_uint8_variable_for_data("v", "abcabcabcabc", max_line_length=20)
    'static uint8_t v[12] = {\n  0x61, 0x62, 0x63,\n  0x61, 0x62, 0x63,\n  0x61, 0x62, 0x63,\n  0x61, 0x62, 0x63,\n}; // v'
    """
    hex_components = []
    for byte in data:
        byte_as_hex = "0x{u:02X}".format(u=ord(byte))
        hex_components.append(byte_as_hex)

    chunk_size = (max_line_length - indent + 2 - 1) // 6  # 6 is len("0xAA, "); +2 for the last element's ", "; -1 for the trailing comma

    array_lines = []
    for chunk_offset in xrange(0, len(hex_components), chunk_size):
        chunk = hex_components[chunk_offset:chunk_offset + chunk_size]
        array_lines.append(" " * indent + ", ".join(chunk) + ",")

    array_data = "\n".join(array_lines)

    if comment != "":
        comment = " // " + comment

    substitutions = {"v": variable_name,
                     "l": len(hex_components),
                     "d": array_data,
                     "c": comment}
    declaration = "static uint8_t {v}[{l}] = {{{c}\n{d}\n}}; // {v}".format(**substitutions)
    return declaration


def write_file(output_directory, filename, contents, overwrite_delay=0):
    try:
        os.makedirs(output_directory)
    except OSError:
        pass  # directory already exists
    outpath = os.path.join(output_directory, filename)
    if os.path.isfile(outpath):
        if overwrite_delay > 0:
            print "Warning: Overwriting {h} in {n} seconds..".format(h=outpath, n=overwrite_delay)
            time.sleep(overwrite_delay)
    with open(outpath, "wb") as outfile:
        outfile.write(contents)
    return outpath


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_directories", help="directory(ies) containing files to bundle, comma-separated; the exact filenames and subdirectory structure will be preserved (useful e.g. for .lproj subdirs)")
    parser.add_argument("output_directory", help="where to write the generated code files")
    parser.add_argument("-c", "--class-name", default="BalerBundle", help="class name (and filename!) for generated code")
    parser.add_argument("-d", "--overwrite-delay", type=int, default=3, help="delay (for frantic cancelling) before overwriting existing files")
    parser.add_argument("-z", "--do-not-compress", action="store_false", dest="compress", help="disable zlib compression (perhaps b/c it doesn't help or libz is not available)")
    args = parser.parse_args(argv)

    if not args.class_name.isalnum():
        print "Classnames must be alphanumeric. You provided `{c}`.".format(c=args.class_name)
        return 1

    print "Processing {i} into {o}".format(i=args.input_directories, o=args.output_directory)
    print

    input_directories_list = args.input_directories.split(',')

    # binary_blobs should really be a dict, but we want the generated file to be stable,
    # which means order preservation, so we use a list of lists instead. Yes, Python
    # 2.7 has an OrderedDict, but there are lots of 2.6 users out there, and it's still
    # not clear that biplist respects the order of the OrderedDict during serialization.
    # (How could it, really? There is no ordered NSDictionary.)
    binary_blobs = []
    sha1s = []
    image_paths = []

    for input_directory in input_directories_list:
        paths_to_bundle = sorted(paths_in_directory(input_directory))
        print "Found {n} files to bundle in directory {d}".format(n=len(paths_to_bundle), d=input_directory)

        for path_components in paths_to_bundle:
            filename = path_components[-1]
            relpath = os.path.join(*path_components)
            path = os.path.join(input_directory, *path_components)
            with open(path, "rb") as input_file:
                data = input_file.read()
            binary_blobs.append([relpath, biplist.Data(data)])  # make biplist treat this as binary data, not as text
            sha1s.append([relpath, hashlib.sha1(data).hexdigest()])
            # just do a crude image test for now, so we don't have to require e.g. PIL
            if any(filename.endswith(image_suffix) for image_suffix in (".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG")):
                # only include a single copy of an image:
                if "@" not in filename and "~" not in filename:
                    image_paths.append(relpath)

    encoded = biplist.writePlistToString(binary_blobs)
    static_data = zlib.compress(encoded, 9) if args.compress else encoded

    print "Size of uncompressed data:", len(encoded)
    if args.compress:
        print "Size of compressed data: {size} ({pct:0.1%} of uncompressed)".format(size=len(static_data), pct=len(static_data) / len(encoded))

    script_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
    print script_dir
    j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(script_dir), trim_blocks=True)
    h_template = j2_env.get_template("BalerBundle.h.j2")
    m_template = j2_env.get_template("BalerBundle.m.j2")

    static_data_var = args.class_name + "_data"

    sub = {
        "command": " ".join(argv),
        "classname": args.class_name,
        "static_data": static_uint8_variable_for_data(static_data_var, static_data, comment="Files and corresponding data"),
        "static_data_var": static_data_var,
        "static_data_len": len(static_data),
        "uncompressed_data_len": len(encoded),
        "compressed": args.compress,
        "sha1s": sha1s,
        "image_paths": image_paths,
    }

    for template, suffix in ((h_template, ".h"), (m_template, ".m")):
        rendered = template.render(**sub)
        filename = write_file(args.output_directory, args.class_name + suffix, rendered, overwrite_delay=args.overwrite_delay)
        print "Wrote file", filename


if __name__ == '__main__':
    sys.exit(main())
