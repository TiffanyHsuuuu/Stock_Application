package stock.application.user;

import stock.application.stock.Stock;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.validation.constraints.Size;
import java.util.Iterator;
import java.util.List;


public class User {

    private Integer id;

    private static int index_stock = 1;

    @Size(min=2, message="Name should have at least two characters!")
    private String username;

    @Size(min=6, message="Name should have at least six characters!")
    private String password;

    private List<Stock> stock_lst;

    protected User() { }

    public User(Integer id, String username, String password, List<Stock> stock_lst) {
        super();
        this.id = id;
        this.username = username;
        this.password = password;
        this.stock_lst = stock_lst;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public List<Stock> getStock_lst() {
        return stock_lst;
    }

    public Stock save(Stock stock) {
        if(stock.getIndex() == null)
            stock.setIndex(index_stock++);
        this.stock_lst.add(stock);
        return stock;
    }

    public Stock findStock(int index) {
        for (Stock stock : stock_lst)
            if (stock.getIndex() == index)
                return stock;
        return null;
    }

    public Stock deleteStock(int index) {
        Iterator<Stock> iterator = stock_lst.iterator();
        while(iterator.hasNext()) {
            Stock stock = iterator.next();
            if(stock.getIndex() == index) {
                iterator.remove();
                return stock;
            }
        }
        return null;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", password='" + password + '\'' +
                //", stock_lst=" + stock_lst +
                '}';
    }
}
