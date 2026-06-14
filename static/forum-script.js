const form = document.getElementById('post-form');
const feed = document.getElementById('reply-feed');
const status = document.getElementById('status');

function renderReply(author, message) {
  const item = document.createElement('article');
  item.className = 'reply-item';
  item.innerHTML = `
    <div class="post-meta">
      <strong>${author}</strong>
      <span>Just now</span>
    </div>
    <p>${message}</p>
  `;
  feed.appendChild(item);
}

function loadPosts() {
  fetch('/api/forum-posts')
    .then((response) => response.json())
    .then((data) => {
      feed.innerHTML = '<h3>Recent replies</h3>';
      data.posts.forEach((post) => renderReply(post.author, post.message));
      status.textContent = data.posts.length
        ? 'Loaded saved forum notes from the text file.'
        : 'No notes yet. Add the first one above.';
    })
    .catch(() => {
      status.textContent = 'Unable to load forum notes right now.';
    });
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const author = document.getElementById('author').value.trim();
  const message = document.getElementById('message').value.trim();

  if (!author || !message) {
    status.textContent = 'Please enter both your name and a message.';
    return;
  }

  try {
    const response = await fetch('/forum_details', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ author, message })
    });

    if (!response.ok) {
      throw new Error('Save failed');
    }

    form.reset();
    loadPosts();
    status.textContent = 'Your note has been saved and will stay on the page.';
  } catch (error) {
    status.textContent = 'Unable to save your note right now.';
  }
});

loadPosts();
