const form = document.getElementById('post-form');
const feed = document.getElementById('reply-feed');
const status = document.getElementById('status');

function addReply(author, message) {
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

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const author = document.getElementById('author').value.trim();
  const message = document.getElementById('message').value.trim();

  if (!author || !message) {
    status.textContent = 'Please enter both your name and a message.';
    return;
  }

  addReply(author, message);
  form.reset();
  status.textContent = 'Your note has been added to the board.';
});
