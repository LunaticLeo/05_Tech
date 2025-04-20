'use strict';

class TaskManager {
	constructor(tasksCount) {
		this.tasksCount = tasksCount;
		this.posts = []; // Using an array instead of a Map
	}

	// Adds engagement data for a post
	addTask(postId, country, likes, shares) {
		let post = this.posts.find(p => p.postId === postId);
		if (!post) {
			post = { postId, data: [] };
			this.posts.push(post);
		}

		let countryData = post.data.find(entry => entry.country === country);
		if (!countryData) {
			countryData = { country, likes: 0, shares: 0 };
			post.data.push(countryData);
		}

		countryData.likes += likes;
		countryData.shares += shares;
	}

	// Analyzes post engagement
	analyzePostLikesAndShares() {
		let globalLikes = new Map();
		let globalShares = new Map();
		let postResults = [];

		for (let post of this.posts) {
			let mostLikedCount = 0,
				mostSharedCount = 0;
			let mostLikedCountries = [],
				mostSharedCountries = [];

			for (let entry of post.data) {
				// Track global statistics
				globalLikes.set(entry.country, (globalLikes.get(entry.country) || 0) + entry.likes);
				globalShares.set(entry.country, (globalShares.get(entry.country) || 0) + entry.shares);

				// Find most liked countries per post
				if (entry.likes > mostLikedCount) {
					mostLikedCount = entry.likes;
					mostLikedCountries = [entry.country];
				} else if (entry.likes === mostLikedCount) {
					mostLikedCountries.push(entry.country);
				}

				// Find most shared countries per post
				if (entry.shares > mostSharedCount) {
					mostSharedCount = entry.shares;
					mostSharedCountries = [entry.country];
				} else if (entry.shares === mostSharedCount) {
					mostSharedCountries.push(entry.country);
				}
			}

			postResults.push({
				postId: post.postId,
				mostLikedCountries: mostLikedCountries.join(', '),
				mostSharedCountries: mostSharedCountries.join(', ')
			});
		}

		// Determine global most liked and shared countries
		const getMaxCountries = map => {
			let maxCount = 0,
				maxCountries = [];
			for (let [country, count] of map.entries()) {
				if (count > maxCount) {
					maxCount = count;
					maxCountries = [country];
				} else if (count === maxCount) {
					maxCountries.push(country);
				}
			}
			return maxCountries.join(', ');
		};

		return {
			postResults,
			globalMostLikedCountries: getMaxCountries(globalLikes),
			globalMostSharedCountries: getMaxCountries(globalShares)
		};
	}

	// Formats and lists the order of engagement analysis
	listOrder() {
		const analysis = this.analyzePostLikesAndShares();
		let report = [];

		analysis.postResults.forEach(post => {
			report.push(`PostId: ${post.postId}`);
			report.push(`Most liked countries in Post ${post.postId}: ${post.mostLikedCountries}`);
			report.push(`Most shared countries in Post ${post.postId}: ${post.mostSharedCountries}`);
			report.push(''); // Empty line for better readability
		});

		report.push(`Global Most Liked Countries: ${analysis.globalMostLikedCountries}`);
		report.push(`Global Most Shared Countries: ${analysis.globalMostSharedCountries}`);

		return report.join('\n');
	}
}

// Example Usage
const taskManager = new TaskManager();
taskManager.addTask(201, 'USA', 300, 1);
taskManager.addTask(201, 'UK', 250, 150);
taskManager.addTask(201, 'Ind', 300, 200);
taskManager.addTask(201, 'Can', 180, 50);
taskManager.addTask(202, 'USA', 200, 120);
taskManager.addTask(202, 'UK', 300, 180);
taskManager.addTask(202, 'Ind', 150, 90);
taskManager.addTask(202, 'Can', 50, 30);
taskManager.addTask(203, 'USA', 500, 250);
taskManager.addTask(203, 'UK', 400, 200);
taskManager.addTask(203, 'Ind', 300, 150);
taskManager.addTask(203, 'Can', 200, 100);

console.log(taskManager.listOrder());
