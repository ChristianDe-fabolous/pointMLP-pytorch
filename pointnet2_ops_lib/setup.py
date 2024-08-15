import glob
import os
import os.path as osp

from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

this_dir = osp.dirname(osp.abspath(__file__))
_ext_src_root = osp.join("pointnet2_ops", "_ext-src")
_ext_sources = glob.glob(osp.join(_ext_src_root, "src", "*.cpp")) + glob.glob(
    osp.join(_ext_src_root, "src", "*.cu")
)
_ext_headers = glob.glob(osp.join(_ext_src_root, "include", "*"))

requirements = ["torch>=1.4"]

exec(open(osp.join("pointnet2_ops", "_version.py")).read())

os.environ["TORCH_CUDA_ARCH_LIST"] = "3.7+PTX;5.0;6.0;6.1;6.2;7.0;7.5"
setup(
    name="pointnet2_ops",
    version=__version__,
    author="Erik Wijmans",
    packages=find_packages(),
    install_requires=requirements,
    ext_modules=[
        CUDAExtension(
            name="pointnet2_ops._ext",
            sources=_ext_sources,
            extra_compile_args={
                "nvcc": [
                    "-O3",
                    "-Xfatbin",
                    "-compress-all",
                    "-gencode", "arch=compute_37,code=sm_37",
                    "-gencode", "arch=compute_50,code=sm_50",
                    "-gencode", "arch=compute_60,code=sm_60",
                    "-gencode", "arch=compute_61,code=sm_61",
                    "-gencode", "arch=compute_62,code=sm_62",
                    "-gencode", "arch=compute_70,code=sm_70",
                    "-gencode", "arch=compute_75,code=sm_75",  # Added for RTX 2080 Ti
                ],
            },
            include_dirs=[osp.join(this_dir, _ext_src_root, "include")],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
    include_package_data=True,
)
