import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

console.log('NYC TLC Analytics - Starting application...');

bootstrapApplication(AppComponent, appConfig)
  .then(() => console.log('NYC TLC Analytics - Application started successfully'))
  .catch((err) => {
    console.error('NYC TLC Analytics - Bootstrap error:', err);
    // Display error on page for debugging
    document.body.innerHTML = `
      <div style="padding: 20px; background: #fee; border: 2px solid #c00; margin: 20px; border-radius: 8px;">
        <h1 style="color: #c00;">Application Failed to Start</h1>
        <p><strong>Error:</strong> ${err.message || err}</p>
        <pre style="background: #f5f5f5; padding: 10px; overflow: auto;">${err.stack || ''}</pre>
        <p>Check the browser console for more details.</p>
      </div>
    `;
  });
