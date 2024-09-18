import {LitElement, html, css} from 'lit';
import {customElement, property} from 'lit/decorators.js';

@customElement('about-page')
class AboutPage extends LitElement {
    override render() {
        return html`
            <p>About page</p>
        `;
      }
}