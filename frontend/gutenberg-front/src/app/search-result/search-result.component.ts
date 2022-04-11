import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { Book } from '../models/book.model';
import { BackendService } from '../services/backend/backend.service';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit {

  books: Book[] = []

  constructor(private router: Router,
    private back: BackendService) {
      const params = this.router.getCurrentNavigation()?.extras.state
      console.log(this.router.getCurrentNavigation())
      if(params) {
        this.retrieveSearchResults(params)
      } else {
        this.router.navigateByUrl('/home')
      }
  }


  ngOnInit(): void {
  }

  async getSearchResults(params: any): Promise<any> {
    switch (params.searchType) {
      case 0:
        return await firstValueFrom(this.back.simpleSearch(params.word, params.user_id))
    
      case 1:
        return await firstValueFrom(this.back.multipleWordsSearch(params.words, params.user_id))

      case 2:
        return await firstValueFrom(this.back.advancedToken(params.regex, params.user_id))

      case 3:
        return await firstValueFrom(this.back.advancedFullText(params.regex, params.user_id))

      default:
        break;
    }
  }

  retrieveSearchResults(params: any) {
    const promise = this.getSearchResults(params)

    promise.then(
      books => {
        books.forEach((book: any) => {
          this.books.push({ id: book.id, title: book.title, author: book.author_name })
        })
      },
      error => {
        console.log(error)
      }
    )
  }

  consultBook(id: string) {
    this.router.navigate(['/book/' + id])
  }

}
