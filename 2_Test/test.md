# JavaScript/TypeScript: Tracking Post Engagement by Region (Likes and Shares)

## Problem Statement

ByteDance, the parent company of TikTok, is looking for an efficient solution to analyze user engagement data across various social media posts. Given the massive volume of data from different countries, they developed a custom `TaskManager` class to handle the processing of this data and generate useful insights.

The class analyzes post engagement by tracking the number of **likes** and **shares** across different regions, as well as globally. It then generates reports to help the platform understand its user engagement trends.

The `TaskManager` class works with posts that contain engagement data like the number of **likes** and **shares** from different countries. Each post is associated with a unique **post ID**, and engagement data for each country is logged.

---

## **Function Description**

Complete the `TaskManager` class in the editor below. The class should have the following methods:

### **1. addTask(postId, country, likes, shares)**

- **Adds** engagement data (**likes and shares**) for a specific country to a given post identified by `postId`.
- **If the post does not already exist**, a new post is created.

### **2. analyzePostLikesAndShares()**

- **Analyzes the engagement data** for all posts.
- Computes:
  - The **most liked** and **most shared** countries for each post.
  - The **most liked** and **most shared** countries **globally** across all posts.
- **Returns** an object containing the detailed results for each post and the global engagement statistics.

### **3. listOrder()**

- Calls the `analyzePostLikesAndShares` function to get the analysis results.
- Formats the output into a readable report.
- **Returns** a formatted string with:
  - The engagement results for each post.
  - The **global most liked** and **most shared** countries.

---

## **Function Parameters**

The function `addTask()` takes the following parameters:

| Parameter | Type   | Description                                            |
| --------- | ------ | ------------------------------------------------------ |
| `postId`  | number | The unique identifier for the post.                    |
| `country` | string | The name of the country providing the engagement data. |
| `likes`   | number | The number of **likes** from the specified country.    |
| `shares`  | number | The number of **shares** from the specified country.   |

### **Returns:**

- **`addTask()`**: This function does not return any value. It adds engagement data (**likes and shares**) to an existing post or creates a new post if it doesn’t already exist. The operation is purely **side-effect-based**.
- **`analyzePostLikesAndShares()`**: This function returns an object containing:
  - `postResults`: An array of objects, each representing a post's engagement analysis.
    - `postId`: The **ID** of the post.
    - `mostLikedCountries`: A string listing the countries with the **most likes** for that post (comma-separated).
    - `mostSharedCountries`: A string listing the countries with the **most shares** for that post (comma-separated).
  - `globalMostLikedCountries`: A string listing the **most liked** countries across **all posts** (comma-separated).
  - `globalMostSharedCountries`: A string listing the **most shared** countries across **all posts** (comma-separated).
- **`listOrder()`**: This function returns an **array of strings**, which is a formatted report of the engagement analysis for each post and **global statistics**.

The report includes:

- A **summary of each post**, showing its **ID**, **most liked countries**, and **most shared countries**.
- A **global summary** of the most liked and most shared countries **across all posts**.

---

## **Example**

Input

```
3
5
201 USA 300 1
201 UK 250 150
201 Ind 300 200
2e1 Can 180 50
202 USA 200 120
202 UK 300 180
202 Ind 150 90
202 Can 50 30
203 USA 500 250
203 UK 400 200
203 Ind 300 150
203 Can 200 100
```

### **Input:**

```
PostId:201
Most liked countries in Post 201: USA, Ind
Most shared countries in Post 201: Ind
PostId:202
Most liked countries in Post 202: UK
Most shared countries in Post 202:UK
PostId: 203
Most liked countries in Post 203: USA
Most shared countries in Post 203: USA
Global Most Liked Countries: USA
Global Most Shared Countries: UK
```
