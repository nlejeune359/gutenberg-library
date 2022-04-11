import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { BackendService } from '../services/backend/backend.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  searchForm: any

  // advancedSearch: boolean = false
  // advancedSearchOption: number = 0

  // search: String = ""

  suggestions: any[] = []

  constructor(private router: Router,
    private fb: FormBuilder,
    private back: BackendService) {
      this.searchForm = this.fb.group({
        search: ['', Validators.required],
        advancedSearch: [false, Validators.required],
        advancedSearchOption: [0, Validators.required],
      })

      this.fetchSuggestions()
    }

  ngOnInit(): void {
  }

  fetchSuggestions() {
    const user_id = localStorage.getItem('id') 
    if(user_id == null) {
      console.log("NO USER_ID")
      return ;
    }

    this.back.getSuggestions(user_id).subscribe(
      suggs => {
        suggs.forEach((suggestion: any) => {
          this.suggestions.push(suggestion)
        })
      }
    )
  }

  searchRequest() {
    console.log("HERE")
    if(this.searchForm.invalid) {
      console.log("FORM INVALID")
      return ;
    }

    const user_id = localStorage.getItem('id') 
    if(user_id == null) {
      console.log("NO USER_ID")
      return ;
    }

    const search: string = this.searchForm.get('search').value

    if(this.searchForm.get('advancedSearch').value) {
      console.log(this.searchForm.get('advancedSearchOption').value)
      switch (this.searchForm.get('advancedSearchOption').value) {
        case '1':
          console.log("CASE 1")
          this.router.navigate(['/search'], {state: {user_id: user_id, regex: search, searchType: 2}})
          break;

        case '2':
          console.log("CASE 2")
          this.router.navigate(['/search'], {state: {user_id: user_id, regex: search, searchType: 3}})
          break;
      
        default:
          console.log("BREAK")
          return ;
      }
    } 
    else {
      if(search.includes(' ')) {
          console.log("MULTIPLE WORDS")
          this.router.navigate(['/search'], {state: {user_id: user_id, words: search, searchType: 1}})
      } 
      else {
          console.log("SIMPLE SEARCH")
          this.router.navigate(['/search'], {state: {user_id: user_id, word: search, searchType: 0}})
      }
    }
  }

  consultBook(id: string) {
    this.router.navigate(['/book/' + id])
  }
}
