export class Piece {
    owner!: number
    king: boolean

    constructor(newOwner: number) {
        this.setOwner(newOwner)
        this.king = false
    }

    public setOwner(newOwner: number) {
        if (newOwner >= 0 && newOwner <= 2) {
            this.owner = newOwner
        }
        else {
            this.owner = 0
        }
    }

    public setKing(newKing: boolean) {
        this.king = newKing
    }

    public getOwner() {
        return this.owner
    }

    public isKing() {
        return this.king
    }
    
}