import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  search: String = ""

  suggestions: String[] = [
    "Suggestion 1",
    "Suggestion 2",
    "Suggestion 3",
    "Suggestion 4",
    "Suggestion 5",
    "Suggestion 6",
    "Suggestion 7"
  ]

  constructor() { }

  ngOnInit(): void {
  }

}
