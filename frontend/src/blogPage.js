var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import './blogHeader';
import './blogFooter';
let BlogPage = class BlogPage extends LitElement {
    constructor() {
        super(...arguments);
        this.posts = [
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
                date: '9 Août 2024',
                summary: 'Résumé du troisième article de blog...',
                link: '#',
            },
            {
                title: 'Quatrième article de blog',
                date: '7 Août 2024',
                summary: 'Résumé du quatrième article de blog, avec une longue phrase pour voir si ça casse pas tout',
                link: '#',
            },
            {
                title: 'Cinquième article de blog',
                date: '6 Août 2024',
                summary: 'Résumé du cinquième article de blog...',
                link: '#',
            },
            {
                title: 'Sixième article de blog',
                date: '5 Août 2024',
                summary: 'Résumé du sixième article de blog...',
                link: '#',
            },
            {
                title: 'Septième article de blog',
                date: '4 Août 2024',
                summary: 'Résumé du septième article de blog...',
                link: '#',
            },
            {
                title: 'Huitième article de blog',
                date: '3 Août 2024',
                summary: 'Résumé du huitième article de blog...',
                link: '#',
            },
            {
                title: 'Neuvième article de blog',
                date: '2 Août 2024',
                summary: 'Résumé du neuvième article de blog...',
                link: '#',
            },
        ];
    }
    static { this.styles = css `
    :host {
      font-family: Arial, sans-serif;
      font-size: 1rem;
    }

    main {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      grid-gap: 1rem;
      padding: 1rem;
    }

    .post {
      padding: 1rem;
      border: 1px solid #ddd;
      border-radius: 5px;
      background-color: #f9f9f9;
    }

    .post h2 {
      margin-top: 0;
      color: #2c3e50;
    }

    .post .date {
      color: #888;
    }

    .post p {
      color: #333;
    }

    .post a {
      color: #1abc9c;
      text-decoration: none;
    }

    .post a:hover {
      text-decoration: underline;
    }
  `; }
    render() {
        return html `
      <blog-header></blog-header>
      <main>
        ${this.posts.map((post) => html `
            <div class="post">
              <h2>${post.title}</h2>
              <div class="date">${post.date}</div>
              <p>${post.summary}</p>
              <a href="${post.link}">Lire la suite</a>
            </div>
          `)}
      </main>
      <blog-footer></blog-footer>
    `;
    }
};
__decorate([
    property({ type: Array })
], BlogPage.prototype, "posts", void 0);
BlogPage = __decorate([
    customElement('blog-page')
], BlogPage);
//# sourceMappingURL=blogPage.js.map