const feedContainer = document.getElementById('feed-container');
const postInput = document.getElementById('create-post');
const createPostForm = document.querySelector('.create-post');

const posts = [
    {
        name: 'Lana Rose',
        handle: '@lanarose',
        time: '15 mins ago',
        image: 'https://picsum.photos/600/400?random=1',
        caption: 'Enjoying the sunset in Dubai. 🌇 #travel #sunset',
        liked: false
    },
    {
        name: 'John Doe',
        handle: '@johndoe',
        time: '2 hrs ago',
        image: 'https://picsum.photos/600/400?random=2',
        caption: 'Just launched my new website! Check it out link in bio. 🚀',
        liked: true
    }
];

function renderFeeds() {
    feedContainer.innerHTML = '';
    posts.forEach((post, index) => {
        const feed = document.createElement('div');
        feed.classList.add('feed');
        feed.innerHTML = `
            <div class="head">
                <div class="user">
                    <div class="profile-pic"></div>
                    <div class="ingo">
                        <h3>${post.name}</h3>
                        <small>${post.time}</small>
                    </div>
                </div>
                <span class="edit"><i class="fas fa-ellipsis-h"></i></span>
            </div>

            <div class="photo">
                <img src="${post.image}">
            </div>

            <div class="action-buttons">
                <div class="interaction-buttons">
                    <span><i class="${post.liked ? 'fas' : 'far'} fa-heart" onclick="toggleLike(${index})"></i></span>
                    <span><i class="far fa-comment-dots"></i></span>
                    <span><i class="fas fa-share-alt"></i></span>
                </div>
                <div class="bookmark">
                    <span><i class="far fa-bookmark"></i></span>
                </div>
            </div>

            <div class="caption">
                <p><b>${post.name}</b> ${post.caption}</p>
            </div>
            <div class="comments text-muted">View all comments</div>
        `;
        feedContainer.appendChild(feed);
    });
}

function toggleLike(index) {
    posts[index].liked = !posts[index].liked;
    renderFeeds();
}

createPostForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (postInput.value.trim() !== "") {
        const newPost = {
            name: 'You',
            handle: '@user',
            time: 'Just now',
            image: `https://picsum.photos/600/400?random=${Math.random()}`,
            caption: postInput.value,
            liked: false
        };
        posts.unshift(newPost);
        postInput.value = '';
        renderFeeds();
    }
});

// Init
renderFeeds();
