.PHONY: build-so clean

# Cython .so 빌드 (사내 빌드 환경에서 실행)
build-so:
	python setup.py build_ext --inplace

clean:
	rm -rf build/ *.so *.c
