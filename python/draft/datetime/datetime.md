
![](https://imgs.xkcd.com/comics/iso_8601.png)

# Using ISO 8601 for Dates

Kevin J. Walchko, Phd

4 Apr 2021

---

Python allows you to format your dates easily and in an agreed upon
way by following the ISO 8601 format:

```python
import datetime as dt

dt.date.today().isoformat()  # -> '2021-04-04'
```

# References

- stackexchange: [Generating Unique ID's](https://codereview.stackexchange.com/a/141419)
- wikipedia: [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
