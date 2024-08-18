package:
	pants run generate:generate-client
	pants tailor ::
	pants fmt fix ::
	pants run docs:build-docs