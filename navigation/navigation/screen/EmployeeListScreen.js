// screens/EmployeeListScreen.js
import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import axios from 'axios';

const EmployeeListScreen = ({ navigation }) => {
    const [employees, setEmployees] = useState([]);

    useEffect(() => {
        // Fetch employees from the API
        axios.get('http://localhost:8000/api/employees/')
            .then(response => setEmployees(response.data))
            .catch(error => console.error(error));
    }, []);

    const renderEmployee = ({ item }) => (
        <TouchableOpacity onPress={() => navigation.navigate('EmployeeDetail', { employeeId: item.id })}>
            <View style={styles.employeeItem}>
                <Text style={styles.employeeName}>{item.first_name} {item.last_name}</Text>
            </View>
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            <FlatList
                data={employees}
                renderItem={renderEmployee}
                keyExtractor={item => item.id.toString()}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
        backgroundColor: '#f8f8f8',
    },
    employeeItem: {
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#ddd',
    },
    employeeName: {
        fontSize: 18,
    },
});

export default EmployeeListScreen;
