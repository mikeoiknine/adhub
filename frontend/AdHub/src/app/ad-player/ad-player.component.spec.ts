import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdPlayerComponent } from './ad-player.component';

describe('AdPlayerComponent', () => {
  let component: AdPlayerComponent;
  let fixture: ComponentFixture<AdPlayerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdPlayerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdPlayerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
