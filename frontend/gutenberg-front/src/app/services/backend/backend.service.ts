import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  apiUrl: string = environment.api_url

  constructor(private http: HttpClient) {} 

  helloWorld(): Observable<any> {
    return this.http.get(this.apiUrl)
  }

  /** User */

  createUser(username: string): Observable<any> {
    return this.http.post<any>(this.apiUrl + 'user/create', {username: username})
  }

  getSuggestions(user_id: string): Observable<any> {
    var queryParams = new HttpParams().set("userId", user_id)
    return this.http.get<any>(this.apiUrl + 'user/suggestions', {params: queryParams})
  }

  /** Searches */

  simpleSearch(word: string, user_id: string): Observable<any> {
    var queryParams = new HttpParams().set("userId", user_id)
    return this.http.get<any>(this.apiUrl + 'search/simple/oneword/' + word, {params: queryParams})
  }

  multipleWordsSearch(words: string[], user_id: string): Observable<any> {
    var queryParams = new HttpParams().set("userId", user_id)
    return this.http.get<any>(this.apiUrl + 'search/simple/multiplewords/' + words, {params: queryParams})
  }

  advancedToken(regex: string, user_id: string): Observable<any> {
    var queryParams = new HttpParams().set("userId", user_id)
    return this.http.get<any>(this.apiUrl + 'search/avanced/token/' + regex, {params: queryParams})
  }

  advancedFullText(regex: string, user_id: string): Observable<any> {
    var queryParams = new HttpParams().set("userId", user_id)
    return this.http.get<any>(this.apiUrl + 'search/avanced/fulltext/' + regex, {params: queryParams})
  }

  /** Books */

  getBook(book_id: string, user_id: string): Observable<any> {
    var queryParams = new HttpParams().set("userId", user_id)
    return this.http.get<any>(this.apiUrl + 'books/' + book_id, {params: queryParams})
  }
}

/*
curl -X 'POST' \
  'http://localhost/user/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "user0"
}'
*/