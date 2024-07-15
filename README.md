# Web Scraper for Static and JS Rendered Sites

This repository contains a versatile web scraper capable of handling both statically rendered HTML sites and dynamically rendered JavaScript sites. By combining techniques for traditional HTML scraping with methods for interacting with JavaScript-heavy websites, this single program offers a comprehensive solution for extracting data from a wide range of web sources.

## Features

- **Dual Scraping Modes:** Can processes static HTML or JS-rendered content.
- **Headless Browser Support:** Utilizes headless browsers to render and scrape JavaScript-heavy sites.
- **Easy Configuration:** Simple setup and configuration to specify target URLs and data extraction rules.
- **Efficient Data Extraction:** Optimized for speed and reliability, ensuring accurate data retrieval.
<!-- Extensive Logging: Provides detailed logs for monitoring scraping activities and troubleshooting. -->

## Usage

### 1. Modify the `config.yaml` file as per your requirement.

- The configuration should follow same format as shown in `config.yaml` by default as a sample.
- The `terminator` key in configuration is optional. Only required if you have a specific terminating point to stop scraping.
- The `path` key can have multiple values, in case you want to extract elements from multiple css-selectors.
- The depth of configuration does not matter as long as the depth ends with the key `path`.

### 2. Run the following code

To get the JS-Rendered Content using Headless browser, follow along with the code below:

```python
import asyncio


async def main(vendor: str):
    data = dict()

    parser = HTMLParser(vendor)
    await parser.initialize_browser()
    await parser.get_all_urls()
    for key, url in tqdm(parser.urls.items()):
        await parser.get_content(url)
        data[key] = parser.data

    await parser.close_browser()
    return data


if __name__ == "__main__":
    VENDOR = "<YOUR_VENDOR_NAME>"
    data = asyncio.run(main(VENDOR))
```

To get the Content from static HTML sites/pages, modify the main function as follows:

```python
async def main(vendor: str):
    data = dict()

    parser = HTMLParser(vendor)
    await parser.get_all_urls()
    for key, url in tqdm(parser.urls.items()):
        await parser.get_content(url)
        data[key] = parser.data
    return data
```

If you want to save the content scrapped, you can do that by following the given code snippet:

```python
async def main(vendor: str, output_file: str = ""):
    data = dict()

    parser = HTMLParser(vendor)
    await parser.initialize_browser()
    await parser.get_all_urls()
    for key, url in tqdm(parser.urls.items()):
        await parser.get_content(url)
        data[key] = parser.data

    await parser.close_browser()
    if output_file:
        await save_data(filename=output_file, data=data)
    return data


if __name__ == "__main__":
    VENDOR = "<YOUR_VENDOR_NAME>"
    OUTPUT_FILE = "<PATH_TO_YOUR_JSON_FILE>"
    data = asyncio.run(main(VENDOR, OUTPUT_FILE))
```

> Remember: **YOUR_VENDOR_NAME** should match one in the **config.yaml** file.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.
