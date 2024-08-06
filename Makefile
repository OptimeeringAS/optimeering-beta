SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = dist/docs

generate-client:
	pants run generate:generate-client
	pants tailor optimeering_beta/*
	pants fix fmt optimeering_beta/*

client-docs:
	rm -rf $(BUILDDIR)
	sphinx-build -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

open-client-docs:
	open $(BUILDDIR)/html/index.html