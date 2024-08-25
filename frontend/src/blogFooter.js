var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { LitElement, html, css } from 'lit';
import { customElement } from 'lit/decorators.js';
let BlogFooter = class BlogFooter extends LitElement {
    static { this.styles = css `
    footer {
      padding: 1rem;
      background-color: #333;
      color: #fff;
      text-align: center;
    }

    p {
      margin: 0;
    }
  `; }
    render() {
        return html `
      <footer>
        <p>&copy; 2024 My Blog. All rights reserved.</p>
      </footer>
    `;
    }
};
BlogFooter = __decorate([
    customElement('blog-footer')
], BlogFooter);
//# sourceMappingURL=blogFooter.js.map