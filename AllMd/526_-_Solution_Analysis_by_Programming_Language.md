## Solution: Analysis by Programming Language

In order to look at the number of entries and the number of posts by programming language, we need to make use of the `.groupby()` method. The key is combining `.groupby()` with the TAG column, which holds our categories (the names of the programming languages).

### Total Posts per Language

If we `.sum()` the number of posts, we can see how many posts each programming language has had since the creation of Stack Overflow.

```python
df.groupby('TAG').sum()
```

Output:

| TAG        | POSTS   |
|------------|---------|
| assembly   | 34852   |
| c          | 336042  |
| c#         | 1423530 |
| c++        | 684210  |
| delphi     | 46212   |
| go         | 47499   |
| java       | 1696403 |
| javascript | 2056510 |
| perl       | 65286   |
| php        | 1361988 |
| python     | 1496210 |
| r          | 356799  |
| ruby       | 214582  |
| swift      | 273055  |

### Months of Data per Language

If we `.count()` the entries in each column, we can see how many months of entries exist per programming language. This is important because newer languages like Go and Swift will have fewer months of data.

```python
df.groupby('TAG').count()
```

Output:

| TAG        | DATE | POSTS |
|------------|------|-------|
| assembly   | 144  | 144   |
| c          | 144  | 144   |
| c#         | 145  | 145   |
| c++        | 144  | 144   |
| delphi     | 144  | 144   |
| go         | 129  | 129   |
| java       | 144  | 144   |
| javascript | 144  | 144   |
| perl       | 144  | 144   |
| php        | 144  | 144   |
| python     | 144  | 144   |
| r          | 142  | 142   |
| ruby       | 144  | 144   |
| swift      | 135  | 135   |

Observations:

- Most languages have 144 months of data (12 years).
- C# has 145 months, likely because it had an entry in the very first month (July 2008) and then continued through the entire period.
- Go (129 months), Swift (135 months), and R (142 months) have fewer entries because they are newer or had gaps in data.