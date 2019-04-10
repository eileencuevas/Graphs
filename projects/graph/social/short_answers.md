1. To create 100 users with an average of 10 friends each, how many times would you need to call addFriendship()? Why?
   
    * You would have to call addFriendship() about 500 times. If each user has about 10 friends, you would have to call addFriendship() once for each friend. If there are 100 users, that makes it 100 * 10, which equals 1000. However, calling addFriendship() on two users that that already had that function called on them in a different order would do nothing, as they are already friends, so you can divide the number of calls by 2 which would result in 500 addFriendship() calls.

2. If you create 1000 users with an average of 5 random friends each, what percentage of other users will be in a particular user's extended social network? What is the average degree of separation between a user and those in his/her extended network?

    * The percentage of users that will be in a particular user's extended social network is 5/999, or  0.5%
    * After running getAllSocialPaths(1) 100 times on a graph of 1000 users, the average degree of separation resulted in about 3.97