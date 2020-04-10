package stock.application.user;

import java.net.URI;
import java.util.List;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;
import stock.application.stock.Stock;
import stock.application.stock.StockNotFoundException;

@RestController
public class UserController {
    @Autowired
    private UserDaoService user_service;

    @GetMapping("/users")
    public List<User> retrieveAllUsers(){
        return user_service.findAllUsers();
    }

    @GetMapping("/users/{id}")
    public User retrieveUser(@PathVariable int id) {
        User user = user_service.findUser(id);
        if(user == null)
            throw new UserNotFoundException("id-"+id);
        return user;
    }

    @DeleteMapping("/users/{id}")
    public void deleteUser(@PathVariable int id) {
        User user = user_service.deleteUser(id);
        if(user == null)
            throw new UserNotFoundException("id-"+id);
    }

    @PostMapping("/users")
    public ResponseEntity<Object> createUser(@Valid @RequestBody User user) {
        User savedUser = user_service.save(user);
        URI location = ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{id}")
                .buildAndExpand(savedUser.getId())
                .toUri();
        return ResponseEntity.created(location).build();
    }

    @GetMapping("/users/{id}/stock")
    public List<Stock> retrieveAllStock(@PathVariable int id) {
        return user_service.findUser(id).getStock_lst();
    }

    @GetMapping("/users/{id}/stock/{index}")
    public Stock retrieveStock(@PathVariable int id, @PathVariable int index) {
        Stock stock = user_service.findUser(id).findStock(index);
        if(stock == null)
            throw new StockNotFoundException("User user- "+ id +" and Stock index- "+index+" not found!");
        return stock;
    }

    @DeleteMapping("/users/{id}/stock/{index}")
    public void deleteStock(@PathVariable int id, @PathVariable int index) {
        Stock stock = user_service.findUser(id).deleteStock(index);
        if(stock == null)
            throw new StockNotFoundException("User user- "+ id +" and Stock index- "+index+" not found!");
    }

    @PostMapping("/users/{id}/stock")
    public ResponseEntity<Object> createStock(@PathVariable int id, @Valid @RequestBody Stock stock) {
        Stock savedStock = user_service.findUser(id).save(stock);
        URI location = ServletUriComponentsBuilder
                .fromCurrentRequest()
                .path("/{index}")
                .buildAndExpand(savedStock.getIndex())
                .toUri();
        return ResponseEntity.created(location).build();
    }
}
