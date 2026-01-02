// ============================================
// BLOG APPLICATION - FULL IMPLEMENTATION
// ============================================

// --- DATA MODEL & STORAGE ---
class BlogPost {
    constructor(title, content, category = 'Thoughts', id = null) {
        this.id = id || Date.now();
        this.title = title;
        this.content = content;
        this.category = category;
        this.createdAt = new Date().toISOString();
        this.updatedAt = new Date().toISOString();
    }
}

class BlogStorage {
    static STORAGE_KEY = 'minimalist_blog_posts';

    static getPosts() {
        const posts = localStorage.getItem(this.STORAGE_KEY);
        return posts ? JSON.parse(posts) : this.getDefaultPosts();
    }

    static savePosts(posts) {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(posts));
    }

    static getDefaultPosts() {
        return [
            new BlogPost(
                "The Art of Minimalism",
                "Minimalism isn't just about owning less; it's about holding space for what matters. In web design, this translates to clean lines, intentional whitespace, and focusing on content over decoration. Every element should serve a purpose. Remove the unnecessary, and what remains becomes profound.",
                "Design"
            ),
            new BlogPost(
                "Understanding Color Theory",
                "Colors evoke emotion. A subtle shift from cool blue to warm orange can completely change the user's perception of a brand. Blue conveys trust and professionalism, making it ideal for corporate sites. Orange radiates energy and creativity. Understanding the psychology behind color choices helps designers make intentional decisions that resonate with their audience.",
                "Design"
            ),
            new BlogPost(
                "Why Vanilla JS?",
                "In an era of frameworks, going back to basics is refreshing. Vanilla JS is faster, lighter, and helps you understand how the DOM truly works beneath the abstraction layers. When you reach for React or Vue, ask yourself: do I really need this? Often, a few lines of vanilla JavaScript can accomplish what a heavy framework does, with better performance and no dependencies.",
                "Development"
            ),
            new BlogPost(
                "Typography Matters",
                "Good typography is invisible. It guides the reader through the text without friction. Choosing the right typeface pairing is the single most impactful design decision you can make. Serif fonts like Merriweather provide elegance and readability for long-form content, while sans-serifs like Open Sans offer clarity for UI elements.",
                "Thoughts"
            )
        ];
    }
}

// --- ROUTER ---
class Router {
    static init() {
        window.addEventListener('hashchange', () => this.handleRoute());
        window.addEventListener('load', () => this.handleRoute());
    }

    static handleRoute() {
        const hash = window.location.hash.slice(1) || 'home';
        const [route, param] = hash.split('/');

        // Hide all views
        document.querySelectorAll('.view').forEach(view => view.classList.add('hidden'));

        switch (route) {
            case 'home':
                BlogApp.showHome();
                break;
            case 'post':
                BlogApp.showPost(parseInt(param));
                break;
            case 'new':
                BlogApp.showForm();
                break;
            case 'edit':
                BlogApp.showForm(parseInt(param));
                break;
            default:
                BlogApp.showHome();
        }

        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === `#${route}`);
        });
    }
}

// --- MAIN APPLICATION ---
class BlogApp {
    static posts = [];
    static filteredPosts = [];
    static searchQuery = '';
    static categoryFilter = 'all';

    static init() {
        this.posts = BlogStorage.getPosts();
        this.filteredPosts = this.posts;

        // If no posts in localStorage, save defaults
        if (!localStorage.getItem(BlogStorage.STORAGE_KEY)) {
            BlogStorage.savePosts(this.posts);
        }

        this.setupEventListeners();
        Router.init();
    }

    static setupEventListeners() {
        // Search
        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.searchQuery = e.target.value.toLowerCase();
            this.filterPosts();
        });

        // Category Filter
        document.getElementById('categoryFilter').addEventListener('change', (e) => {
            this.categoryFilter = e.target.value;
            this.filterPosts();
        });

        // Form Submit
        document.getElementById('postForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });

        // Character Count
        document.getElementById('postContent').addEventListener('input', (e) => {
            document.getElementById('charCount').textContent = e.target.value.length;
        });

        // Single Post Actions
        document.getElementById('editPostBtn').addEventListener('click', () => {
            const postId = parseInt(document.getElementById('singlePost').dataset.postId);
            window.location.hash = `#edit/${postId}`;
        });

        document.getElementById('deletePostBtn').addEventListener('click', () => {
            const postId = parseInt(document.getElementById('singlePost').dataset.postId);
            this.deletePost(postId);
        });
    }

    static filterPosts() {
        this.filteredPosts = this.posts.filter(post => {
            const matchesSearch =
                post.title.toLowerCase().includes(this.searchQuery) ||
                post.content.toLowerCase().includes(this.searchQuery);

            const matchesCategory =
                this.categoryFilter === 'all' ||
                post.category === this.categoryFilter;

            return matchesSearch && matchesCategory;
        });

        this.renderPosts();
    }

    // --- VIEW RENDERING ---
    static showHome() {
        document.getElementById('homeView').classList.remove('hidden');
        this.filterPosts();
    }

    static showPost(postId) {
        const post = this.posts.find(p => p.id === postId);
        if (!post) {
            window.location.hash = '#home';
            return;
        }

        const container = document.getElementById('singlePost');
        container.dataset.postId = postId;

        const date = new Date(post.createdAt).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        container.innerHTML = `
            <div class="blog-post single">
                <span class="category-badge">${post.category}</span>
                <h1>${post.title}</h1>
                <span class="meta">Posted on ${date}</span>
                <div class="post-content">${post.content}</div>
            </div>
        `;

        document.getElementById('postView').classList.remove('hidden');
    }

    static showForm(editPostId = null) {
        const form = document.getElementById('postForm');
        const formTitle = document.getElementById('formTitle');

        if (editPostId) {
            const post = this.posts.find(p => p.id === editPostId);
            if (!post) {
                window.location.hash = '#home';
                return;
            }

            formTitle.textContent = 'Edit Post';
            document.getElementById('postTitle').value = post.title;
            document.getElementById('postCategory').value = post.category;
            document.getElementById('postContent').value = post.content;
            document.getElementById('charCount').textContent = post.content.length;
            form.dataset.editId = editPostId;
        } else {
            formTitle.textContent = 'Create New Post';
            form.reset();
            document.getElementById('charCount').textContent = '0';
            delete form.dataset.editId;
        }

        document.getElementById('formView').classList.remove('hidden');
    }

    static renderPosts() {
        const container = document.getElementById('blogPosts');

        if (this.filteredPosts.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>No posts found</h3>
                    <p>Try adjusting your search or filter.</p>
                </div>
            `;
            return;
        }

        // Sort by date (newest first)
        const sortedPosts = [...this.filteredPosts].sort((a, b) =>
            new Date(b.createdAt) - new Date(a.createdAt)
        );

        container.innerHTML = sortedPosts.map(post => {
            const date = new Date(post.createdAt).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });

            const excerpt = post.content.length > 200
                ? post.content.substring(0, 200) + '...'
                : post.content;

            return `
                <article class="blog-post">
                    <span class="category-badge">${post.category}</span>
                    <h2>${post.title}</h2>
                    <span class="meta">Posted on ${date}</span>
                    <p>${excerpt}</p>
                    <a href="#post/${post.id}" class="read-more">Read Full Article &rarr;</a>
                </article>
            `;
        }).join('');
    }

    // --- CRUD OPERATIONS ---
    static handleFormSubmit() {
        const form = document.getElementById('postForm');
        const title = document.getElementById('postTitle').value.trim();
        const category = document.getElementById('postCategory').value;
        const content = document.getElementById('postContent').value.trim();

        if (!title || !content) return;

        const editId = form.dataset.editId;

        if (editId) {
            // Update existing post
            const post = this.posts.find(p => p.id === parseInt(editId));
            if (post) {
                post.title = title;
                post.category = category;
                post.content = content;
                post.updatedAt = new Date().toISOString();
            }
        } else {
            // Create new post
            const newPost = new BlogPost(title, content, category);
            this.posts.unshift(newPost);
        }

        BlogStorage.savePosts(this.posts);
        window.location.hash = '#home';
    }

    static deletePost(postId) {
        if (!confirm('Are you sure you want to delete this post?')) return;

        this.posts = this.posts.filter(p => p.id !== postId);
        BlogStorage.savePosts(this.posts);
        window.location.hash = '#home';
    }
}

// --- INITIALIZE APPLICATION ---
document.addEventListener('DOMContentLoaded', () => {
    BlogApp.init();
});
