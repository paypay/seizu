# Contributing

## Code of conduct

This project is governed by PayPay’s [code of conduct](https://paypay.github.com/seizu/dev/code-of-conduct.html). All contributors and participants agree to abide by its terms.

## Contributing code

### File issues in Github

In general all enhancements or bugs should be tracked via github issues before PRs are submitted.
We don’t require them, but it’ll help us plan and track.

When submitting bugs through issues, please try to be as descriptive as possible.
It’ll make it easier and quicker for everyone if the developers can easily reproduce your bug.

### Submit pull requests

Our only method of accepting code changes is through github pull requests.

### Update the changelog

We track changes in a changelog so that users can quickly see changes between releases.
As part of your pull requests, please also update the newest unreleased version's changelog with the changes in your pull request.
You should also add your github username, to be recognized for the contribution.

### Sign the Contributor License Agreement (CLA)

We require a CLA for code contributions, so before we can accept a pull request we need to have a signed CLA.
When you open your first pull request, the CLA will show up as a test.
Please follow the test's link to sign the CLA, if you haven't done so yet.

## Release process

### Determining release version

We version our releases based on semantic versioning.
When cutting a new release, please keep in mind which version number should be bumped.
As a general guide, here's when you should bump each versison type:

* Major: When a backwards incompatible change is made. For example:
  * Backwards incompatible change to the configuration file format.
  * Backwards incompatible change to a pluggable system (like the action plugins).
  * Backwards incompatible change to one of the auth methods.
* Minor: Any new feature or bug fix.
* Point: Documentation changes, or packaging fix, or cosmetic (non-functionality) changes.

### Cutting the release

1. First, update the changelog, so that it properly reflects the version we're going to release.
1. Next, go to the [releases page in github](https://github.com/paypay/seizu/releases).
1. Click [Draft a new release](https://github.com/paypay/seizu/releases/new).
1. Click `Choose a tag`, and type in the new tag version, prefixed with a v; example: `v1.0.0`, and click the `Create new tag` dialog under the text.
1. Add a title for the release, and fill in the description with the contents of the release notes for this version.
1. Click `Publish Release`.
