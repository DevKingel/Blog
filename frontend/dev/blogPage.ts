import {LitElement, html, css} from 'lit';
import {customElement, property} from 'lit/decorators.js';
import './blogHeader';
import './blogFooter';

@customElement('blog-page')
class BlogPage extends LitElement {
  @property({type: Array})
  posts = [
    {
      title: 'Premier article de blog',
      date: '12 Août 2024',
      summary: 'Résumé du premier article de blog...',
      link: '#',
    },
    {
      title: 'Deuxième article de blog',
      date: '10 Août 2024',
      summary: 'Résumé du deuxième article de blog...',
      link: '#',
    },
    {
      title: 'Troisième article de blog',
      date: '8 Août 2024',
      summary: 'Résumé du troisième article de blog...',
      link: '#',
    },
  ];

  static override styles = css`
    :host {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      font-family: Arial, sans-serif;
    }

    main {
      flex: 1;
      padding: 1rem;
    }

    .post {
      margin-bottom: 20px;
      padding: 15px;
      border: 1px solid #ddd;
      border-radius: 5px;
      background-color: #f9f9f9;
    }

    .post h2 {
      margin-top: 0;
      font-size: 24px;
      color: #2c3e50;
    }

    .post .date {
      font-size: 14px;
      color: #888;
      margin-bottom: 10px;
    }

    .post p {
      font-size: 16px;
      line-height: 1.5;
      color: #333;
    }

    .post a {
      display: inline-block;
      margin-top: 10px;
      color: #1abc9c;
      text-decoration: none;
    }

    .post a:hover {
      text-decoration: underline;
    }
  `;

  override render() {
    return html`
      <blog-header></blog-header>
      <main>
        ${this.posts.map(
          (post) => html`
            <div class="post">
              <h2>${post.title}</h2>
              <div class="date">${post.date}</div>
              <p>${post.summary}</p>
              <a href="${post.link}">Lire la suite</a>
            </div>
          `
        )}
      </main>
      <blog-footer></blog-footer>
    `;
  }
}
