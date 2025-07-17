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
  otp = '';
  token = '';
  error = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit() {
    this.authService.login(this.username, this.password, this.otp).subscribe({
      next: (response: any) => {
        console.log('Login exitoso:', response);
        this.token = response.token;
        this.error = '';
        // Opcional: redirigir después del login
        // this.router.navigate(['/dashboard']);
      },
      error: () => {
        this.error = 'Credenciales u OTP incorrectos';
        this.token = '';
      }
    });
  }

  goToRegister() {
    this.router.navigate(['/register']);
  }
}
