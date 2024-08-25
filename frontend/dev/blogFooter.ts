import {LitElement, html, css} from 'lit';
import {customElement} from 'lit/decorators.js';

@customElement('blog-footer')
class BlogFooter extends LitElement {
  static override styles = css`
    footer {
      padding: 1rem;
      background-color: #333;
      color: #fff;
      text-align: center;
    }

    p {
      margin: 0;
    }
  `;

  override render() {
    return html`
      <footer>
        <p>&copy; 2024 My Blog. All rights reserved.</p>
      </footer>
    `;
  }
}
