import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { App } from './app/app.component';
import { routes } from './app/app.routes';
import { provideHttpClient } from '@angular/common/http'; // Import provideHttpClient

bootstrapApplication(App, {
    providers: [
        provideRouter(routes, withComponentInputBinding()),
        provideHttpClient() // Provide HttpClient at the application level
    ]
}).catch(err => console.error(err));