SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

client-docs:
	rm -rf $(BUILDDIR)
	sphinx-build -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

open-client-docs:
	open $(BUILDDIR)/html/index.html