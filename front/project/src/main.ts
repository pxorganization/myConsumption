import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { App } from './app/app.component';
import { routes } from './app/app.routes';

bootstrapApplication(App, {
    providers: [
        provideRouter(routes, withComponentInputBinding())
    ]
}).catch(err => console.error(err));