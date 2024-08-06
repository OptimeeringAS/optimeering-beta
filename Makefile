generate-client:
	pants run generate:generate-client
	pants tailor optimeering_beta/*
	pants fix fmt optimeering_beta/*
