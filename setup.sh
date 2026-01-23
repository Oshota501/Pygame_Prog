python -c "import sysconfig; print(sysconfig.get_path('include'))"

cd ./pg3_math/
python setup.py build_ext --inplace
cd ../
