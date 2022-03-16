import argparse
import os.path
import subprocess
from compiler_wrapper import calc_time

import logging

LLVM_KEYS = "-G Ninja -DLLVM_ENABLE_PROJECTS='clang' -DCMAKE_BUILD_TYPE=Debug " \
            "-DLLVM_INCLUDE_EXAMPLES=OFF -DLLVM_INCLUDE_BENCHMARKS=OFF " \
            "-DLLVM_TARGETS_TO_BUILD='X86' -DLLVM_PARALLEL_LINK_JOBS=2 -DLLVM_USE_LINKER=gold"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("root",
                        help="Path to a llvm root folder",
                        type=str,
                        )
    parser.add_argument("recompile",
                        help="Compile llvm/clang again but with compiled clang",
                        type=bool,
                        default=False)
    return parser.parse_args()


@calc_time
def build(command_line: list) -> None:
    subprocess.run(command_line, check=True)
    subprocess.run(['ninja', '-j 10'], check=True)


def main():
    args = get_args()
    logging.info('Start compiling llvm/clang')
    build(['cmake'] + LLVM_KEYS.split() + [args.root])
    if args.recompile:
        path_to_clang = os.path.join(os.path.abspath('bin'), 'clang')
        path_to_clangpp = os.path.join(os.path.abspath('bin'), 'clang++')

        build(['cmake'] + [f'-DCMAKE_C_COMPILER={path_to_clang}',
                           f'-DCMAKE_CXX_COMPILER={path_to_clangpp}',
                           f'-DCMAKE_ASM_COMPILER={path_to_clang}'] + LLVM_KEYS.split() + [args.root])


if __name__ == '__main__':
    main()
