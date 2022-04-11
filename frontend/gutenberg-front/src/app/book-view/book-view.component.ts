import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BackendService } from '../services/backend/backend.service';

@Component({
  selector: 'app-book-view',
  templateUrl: './book-view.component.html',
  styleUrls: ['./book-view.component.scss']
})
export class BookViewComponent implements OnInit {

  bookId: string = ''

  author: string = ''
  title: string = ''
  text: string = ''

  constructor(private route: ActivatedRoute,
    private router: Router,
    private back: BackendService) {
    const param = this.route.snapshot.paramMap.get('book_id');

    if(param == null) {
      this.router.navigate(['/home'])
    } else {
      this.bookId = param
    }

    this.fetchBook()
  }

  fetchBook() {
    const user_id = localStorage.getItem('id') 
    if(user_id == null) {
      this.router.navigate(['home'])
      return ;
    }

    this.back.getBook(this.bookId, user_id).subscribe(
      book => {
        this.author = book.author
        this.title = book.title
        this.text = book.full_text
      }
    )
  }

  ngOnInit(): void {
  }

}
