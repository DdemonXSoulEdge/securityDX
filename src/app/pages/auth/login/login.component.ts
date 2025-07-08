import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  error = '';
  token = ''; 

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit() {
    this.authService.login(this.username, this.password).subscribe({
      next: (response: any) => {
        console.log('Login exitoso:', response);
        this.token = response.token;
        this.error = '';
      },
      error: (err) => {
        this.error = 'Usuario o contraseña incorrectos';
        this.token = '';
      }
    });
  }

  goToRegister() {
    this.router.navigate(['/register']);
  }
}
