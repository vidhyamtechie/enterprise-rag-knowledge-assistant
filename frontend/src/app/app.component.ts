import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface Source {
  source: string;
  page: number | null;
  chunk_id: string;
  distance: number | null;
}

interface ChatResponse {
  answer: string;
  sources: Source[];
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  question = '';

  answer = signal('');
  sources = signal<Source[]>([]);
  loading = signal(false);
  error = signal('');

  private readonly apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  ask(): void {

    if (!this.question.trim()) {
      return;
    }

    this.loading.set(true);
    this.error.set('');
    this.answer.set('');
    this.sources.set([]);

    this.http.post<ChatResponse>(
      `${this.apiUrl}/api/chat`,
      {
        question: this.question
      }
    ).subscribe({

      next: (result) => {

        console.log('RAG response:', result);

        this.answer.set(result.answer);
        this.sources.set(result.sources || []);

        this.loading.set(false);
      },

      error: (err) => {

        console.error('RAG API Error:', err);

        this.error.set(
          'Unable to query the knowledge base.'
        );

        this.loading.set(false);
      }

    });
  }
}