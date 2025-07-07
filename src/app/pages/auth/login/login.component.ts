import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router'; // 👈 Importa Router
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

  constructor(
    private authService: AuthService,
    private router: Router // 👈
  ) {}

  onSubmit() {
    this.authService.login(this.username, this.password).subscribe({
      next: (response) => {
        console.log('Login exitoso:', response);
        // Aquí redirige a donde quieras, por ejemplo:
        // this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.error = 'Usuario o contraseña incorrectos';
      }
    });
  }

  // 👈 Método para navegar al registro
  goToRegister() {
    this.router.navigate(['/register']);
  }
}