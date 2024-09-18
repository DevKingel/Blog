import './assets/blog-header';
import './assets/blog-footer';

import {LitElement, html, css} from 'lit';
import {customElement, property} from 'lit/decorators.js';

@customElement('error-404')
class Error404 extends LitElement {
  override render() {
    return html` <p>404 page</p> `;
  }
}
