
import csv
import numpy as np

def save_csv_file(data, csv_file_name, version, print_out=False):
    """ Save data to a csv_file_name (use it after 'read_from_all_topics').
    """

    # Create csv file
    with open(csv_file_name, mode='w') as csv_file:

        A = np.array(data)
        topics_names_column = A[:,0]
        topics_types_column = A[:,1]

        # Create file header
        csv_file.write(str("file_name = %s \n" %csv_file_name))
        csv_file.write(str("version = %s \n" %version))
        csv_file.write(str("topic_names_count = %s \n" %len(topics_names_column)))
        csv_file.write(str("topics_names = %s \n" %topics_names_column))
        csv_file.write(str("topic_types_count = %s \n" %len(topics_types_column)))
        csv_file.write(str("topics_types = %s \n\n\n" %topics_types_column))

        # print(topics_column)
        # a = list(set(data[:][2]))

        # csv_file.write(str("topic_names = %s \n" %len(data)))

        # Create csv header
        field_names = ['topic_name', 'topic_type', 'time_stamp', 'message']
        writer = csv.DictWriter(csv_file,fieldnames=field_names)
        writer.writeheader()

        # Save data
        for i in range(len(data)):
            topic_name = data[i][0]
            topic_type = data[i][1]

            for j in range(len(data[i][2])):
                writer.writerow({   'topic_name': topic_name,
                                    'topic_type': topic_type, 
                                    'time_stamp': data[i][2][j],
                                    'message': data[i][3][j] })

    if print_out:
        print('Saving', csv_file_name)
