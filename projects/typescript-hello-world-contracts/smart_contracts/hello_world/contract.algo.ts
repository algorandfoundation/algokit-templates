import { Contract } from '@algorandfoundation/algorand-typescript'

export class HelloWorld extends Contract {
  public hello(name: string): string {
    return `${this.getHello()} ${name}`
  }

  private getHello() {
    return 'Hello'
  }
}
