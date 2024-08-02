find ./optimeering_beta -type f -name '*.py' -delete
find ./optimeering_beta -type f -name '*.md' -delete
python ./generation/fix_openapi_extensions.py
java -jar ./generation/openapi-generator-cli.jar generate \
  --input-spec ./generation/openapi.json \
  --generator-name python \
  --output ./ \
  --template-dir ./generation/python_templates \
  --skip-validate-spec \
  --config ./generation/generation_config.config
rm -rf .openapi-generator
rm -rf .openapi-generator-ignore
rm -rf ./optimeering_beta/test
rm -rf ./optimeering_beta/docs
rm ./optimeering_beta_README.md
cp ./generation/azure_authentication.py ./optimeering_beta/azure_authentication.py
pants tailor ::
pants fix fmt ::
