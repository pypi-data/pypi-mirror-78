# check50_checkstyle

This is an extension for the [CS50 automarker check50][check50] that allows to run the static code analyser [checkstyle](https://checkstyle.org) and interpret the resulting XML report as check50 Failures.

Checkstyle let's you complain about style issues, particularly in Java code, beyond what [style50][style50] (astyle) can do.
For instance you can flag if identifiers don't adhere to Java's camelCase code conventions, or javadocs are missing.

For convenience, this package ships with the stand-alone CLI of checkstyle ([`checkstyle-8.35-all.jar`](https://github.com/checkstyle/checkstyle/releases/)), which is why it is so large.

## Example Usage

You need to import this module into your problem set (`__init.py__`):

```python
import check50_checkstyle
```

and declare `#- check50-checkstyle` it as a dependency in your `.cs50.yml` file:

```yml
check50:
  dependencies:
    - check50-checkstyle
```

Checkstyle needs an XML style definition file to run.
The jar file contains two such definitions, following the sun or google style guides but both are rather "picky",i.e., complain about lots of minor stuff. Pick one of these style files and delete what you don't like.

Let's assume your problem set contains the style definition `style.xml`.
Then you add a check50 check as follows. The target can be more specific of course.

```python
@check50.check(exists)
def checkstyle():
    """style police"""
    check50.include("style.xml")
    check50_checkstyle.run_and_interpret_checkstyle(
        checks_file='style.xml',
        target='*.java')

```

This will dump all warnings into the log (because check50 hard-codes its html template). Example output:

```
:( style police
    stylistic issues found
    Issues found:
    - In Credit.java(line 4, char 5): Missing a Javadoc comment.
    - In Basket.java(line 2, char 1): Wrong lexicographical order for 'java.util.ArrayList' import. Should be before 'java.util.List'.
    - In Basket.java(line 19, char 5): Missing a Javadoc comment.
    - In Basket.java(line 27, char 5): Missing a Javadoc comment.
    - In Basket.java(line 35, char 5): Missing a Javadoc comment.
    - In Basket.java(line 47): First sentence of Javadoc is missing an ending period.
    - In Item.java(line 27): Line is longer than 100 characters (found 102).
    - In Item.java(line 53, char 40): 'typecast' is not followed by whitespace.
    - In Snack.java(line 20, char 5): Missing a Javadoc comment.
```



[checkstyle]: https://checkstyle.sourceforge.io/
[check50]: https://github.com/cs50/check50
[style50]: https://cs50.readthedocs.io/style50/
