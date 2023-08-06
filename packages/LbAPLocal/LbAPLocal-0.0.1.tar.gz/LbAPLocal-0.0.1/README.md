# LbAPLocal

LbAPLocal is the python library for running offline tests for the LHCb AnalysisProductions framework.

## Installation

For now it can be installed by running

```bash
python -m pip install git+https://gitlab.cern.ch/lhcb-dpa/analysis-productions/lbaplocal.git
```
In the future it will become available within the LHCb environment,

## Usage

After installing, LbAPLocal can be run from the command line with the following options:

```bash
Usage: lb-ap [OPTIONS] COMMAND [ARGS]...

  Command line tool for the LHCb AnalysisProductions

Options:
  --help  Show this message and exit.

Commands:
  list       List the available production folders by running lb-ap list...
  render     Render the info.yaml for a given production
  reproduce  Reproduce an existing online test locally
  test       Run a local test job for a specific production job
```

To see which productions are available:
```bash
lb-ap list
```

To see which jobs are avaiable for a given production:
```bash
lb-ap list BsToJpsiPhi
```

To render the `info.yaml` for a given production:
```bash
lb-ap render BsToJpsiPhi
```