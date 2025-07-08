import { Routes } from '@angular/router';
import { Error404Component } from './pages/errors/error-404/error-404.component';


export const routes: Routes = [
    {path: '', redirectTo: "/auth/login", pathMatch: 'full'},
    {path:"auth", loadChildren: () => import('./pages/auth/auth.routes').then(n => n.authRoutes)},
    { path: '**', component: Error404Component }

];
