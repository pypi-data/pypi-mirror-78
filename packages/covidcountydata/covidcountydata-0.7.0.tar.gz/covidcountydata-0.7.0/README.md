# covidcountydata

Welcome to the Python client library documentation for the [Covid County Data](https://covidcountydata.org) (CCD) database.


## Installation

The `covidcountydata` Python package is available on the
[Python Package Index (pypi)](https://pypi.org/) and can be installed with `pip`.

```python
pip install covidcountydata
```

## API keys

Our data is free and open for anyone to use (and always will be). Our team agreed that this was
central to our mission when we agreed to begin this project. However, we do find it useful to
have information about our users and to see how they use the data for two reasons:

1. It helps us focus and improve the datasets that are seeing the most use.
2. The number of users, as measured by active API keys, is one metric that we use to show that the
   project is useful when we are discussing additional grant funding.

We are grateful to everyone who is willing to register for and use their API key when interacting
with our data.

To register for an API key, you can register [on our website](https://covidcountydata.org#register)
or from the Python package using the `register` method.

```python
from covidcountydata import Client

c = Client()
c.register()
```

You will be prompted for your email address. After entering a valid email address we will issue
an API key, store it on your machine, and automatically apply it to all future requests made from
Python to our servers.

If at any time you would like to remove your API key, please delete the file `~/.covidcountydata/apikey`.


## Data


### Datasets

You can see a list of the available datasets in our API from the Python library by doing:

```python
from covidcountydata import Client

c = Client()
print(c.datasets)
```

For more information on each of these datasets, we recommend that you visit our
[data documentation page](https://covidcountydata.org/data/documentation).


### Data keys

Many of the datasets in our database are indexed by one or more common "keys". These keys are:

- `vintage`: The date and time that the data was downloaded into our database. We collect this
  because of the rapidly evolving nature of COVID-19 -- It allows us to have a record of when data was
  changed/corrected/updated.
- `dt`: The date and time that an observation corresponds to. For series like COVID tests
  administered this may a daily frequency, but, for others like unemployment it may be a weekly or
  monthly frequency.
- `location`: A geographic identifier for the location. For the counties/states in the dataset,
  this variable corresponds to the Federal Information Processing Standards number.

Whenever two series with common keys are loaded together, they will be merged on their common keys.


### Requesting data

Requesting data using the Python client library involves three steps:


#### 1. Create a client

To create a client, use the `Client` class.

```python
from covidcountydata import Client

c = Client()
```

You can optionally pass in an API key if you have one (see the section on API keys).

```python
c = Client("my api key")
```

If you have previously registered for an API key on your current machine, it will be loaded and
used automatically for you.

In practice you should rarely need to pass the API key by hand unless you are loading the key from
an environment variable or another source.


#### 2. Build a request

Each of the datasets in the API have an associated method.

To add datasets to the current request, call the `Client.dataset()`method. For example, to add
the `covid_us` dataset to the request, you would call:

```python
c.covid_us(state="CA")
```

If you wanted to add another dataset, such as `demographics`, you would simply call that method as
well.

```python
c.demographics()
```

You can see that the printed form of the client is updated to show you what the current request
looks like by printing the current client.

```python
print(c)
```

To clear the current request, use `c.reset()`:

Since each dataset will build up a request for the client and return the client itself, we can
chain together multiple requests. For example, rather than doing the separate commands from above,
we could have done.

```python
c.covid_us(state="CA").demographics()
```

**Filtering data**

Each of the dataset functions has a number of filters that can be applied.

These filters allow you to select certain rows and/or columns.

For example, in the above example we had `c.covid_us(state="CA")`. This instructs the client to
only fetch data for geographic regions that are in the state of California.

**NOTE:** If a filter is passed to one dataset in the request but is applicable to other datasets
in the request, it will be applied to *all* datasets.

For example in `c.covid_us(state="CA").demographics()` we only specify a `state` filter on the
`covid_us` dataset, but when the data is collected it will also be applied to `demographics`.

We do this because we end up doing an inner join on all requested datasets, so when we filter the
state in `covid_us` they also get filtered in `demographics`.


#### 3. Fetch the data

To fetch the data, call the `fetch` method from the client.

```python
df = c.fetch()
```

Note that after a successfully request, the client is reset so there are no "built-up" requests
remaining.



## Examples

We provide a few simple examples here in the README, but you can find additional examples in the `examples` folder.

**Simple Example: Single dataset for all FIPS**

The example below loads all within county mobility data.

```python
import covidcountydata as ccd
c = ccd.Client()

c.mobility_devices()
df = c.fetch()
```


**Simple Example: Single dataset for single county**

The example below loads just demographic information for Travis County in Texas.

Notice that we can select a particular geography by specifying the fips code. We can do similar things for any of the keys listed previously.

```python
c = ccd.Client()
c.demographics(location=48453)
df = c.fetch()
```


**Simple Example: Single dataset for all counties in a state**

The example below loads just demographic information for all counties in Texas.

Notice that we can select a particular geography by specifying the fips code. We can do similar things for any of they keys listed previously.

```python
c = ccd.Client()
c.demographics(state=48)
df = c.fetch()
```

**Simple Example: COVID data since July 1, 2020 for counties in Georgia**

The example below shows how to filter on both a state and a range of dates, fetching only data for July 1st onwards.

```python
c = ccd.Client()
c.covid_us(state="GA", dt=">=2020-07-01")
df = c.fetch()
```


**Intermediate Example: COVID data since July 1, 2020 for counties in Georgia with county info**

This is the same example as above, but we also add on the `us_counties` endpoint. This will cause the returned DataFrame to have
information on the counties including county name, state name, county area, county latitude, and county longitude.

```python
c = ccd.Client()
c.covid_us(state="GA", dt=">=2020-07-01").us_counties()
df = c.fetch()
```


**Intermediate Example: Multiple datasets for single county**

The example below loads covid and demographic data and showcases how to chain calls to multiple datasets together. It will automatically merge and return these datasets.

Note that applying a filter to any of the datasets (in this case `fips=6037`) will apply it to all datasets.

```python
c = ccd.Client()
(
    c
    .covid_us(location=6037)
    .demographics()
)
df = c.fetch()
```


**Advanced Example: Multiple datasets with multiple filters and variable selection**

The example below loads data from three datasets for a particular FIPS code, using a particular date of demographics, and selects certain variables from the datasets.

```python
c = ccd.Client()
(
    c
    .economic_snapshots(variable="GDP_All industry total")
    .covid_us(location=6037)
    .demographics(variable="Total population")
)
df = c.fetch()
```

There are more examples in the `covidcountydata/examples.py` file. We encourage you to explore them and to reach out if you have questions!
