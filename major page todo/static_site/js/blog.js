
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('posts-container');
    const data = await fetchData('blog_posts.json');

    if (!data) {
        container.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: var(--color-red);">Failed to load blog posts.</div>';
        return;
    }

    // Sort by date desc
    const posts = data.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

    // Icon
    const FileText = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" x2="8" y1="13" y2="13"/><line x1="16" x2="8" y1="17" y2="17"/><line x1="10" x2="8" y1="9" y2="9"/></svg>';

    container.innerHTML = posts.map(post => `
        <a href="blog-post.html?slug=${post.slug}" class="blog-card">
            <div class="card-content">
                <div class="icon-box">
                    ${FileText}
                </div>
                <div>
                    <h2 class="post-title">${post.title}</h2>
                    <p class="post-date">${new Date(post.createdAt).toLocaleDateString()}</p>
                    <p class="post-excerpt">${post.excerpt}</p>
                </div>
            </div>
        </a>
    `).join('');
});
