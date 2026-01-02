
document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('post-content');
    const urlParams = new URLSearchParams(window.location.search);
    const slug = urlParams.get('slug');

    if (!slug) {
        window.location.href = 'blog.html';
        return;
    }

    const data = await fetchData('blog_posts.json');
    if (!data) {
        container.innerHTML = '<div style="text-align: center; color: var(--color-red);">Failed to load post.</div>';
        return;
    }

    const post = data.find(p => p.slug === slug);
    if (!post) {
        container.innerHTML = '<div style="text-align: center; color: var(--text-muted);">Post not found.</div>';
        return;
    }

    document.title = `${post.title} - TanTheta`;

    // Use marked library if available, otherwise simple text replacement
    let contentHtml = '';
    if (typeof marked !== 'undefined') {
        contentHtml = marked.parse(post.content);
    } else {
        // Fallback simple markdown parser
        contentHtml = post.content
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
            .replace(/\n/gim, '<br>');
    }

    container.innerHTML = `
        <article class="article-content">
            <h1>${post.title}</h1>
            <div class="publish-date">
                Published on ${new Date(post.createdAt).toLocaleDateString()}
            </div>
            <div>
                ${contentHtml}
            </div>
        </article>
    `;
});
